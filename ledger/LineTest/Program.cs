using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

/// THE LOCAL LINE-WRITING BLIND TEST (checklist L01), 25 September.
///
///     llama-server -m <model>.gguf -ngl 99 --port 8091 --jinja --reasoning-budget 0
///     dotnet run -c Release --project ledger/LineTest -- --local qwen3.5-4b=http://127.0.0.1:8091 [--local ...] [--paid] --out DIR
///     dotnet run -c Release --project ledger/LineTest -- --selftest
///
/// WHY. Writing the lines is about 70 percent of the cost of live talk
/// (production/research/runtime-ai-business), and Jafar made testing a local
/// writer a priority: "the best local writers that fit what the card has left
/// write the same lines as the paid model, shown to Jafar without saying which
/// is which". What the card has left beside the street and the voice was
/// measured on 24 September: about 3.7 GB, so 3 to 4B models at Q4.
///
/// THE SAME PROMPT FOR EVERY WRITER. Each moment builds the game's own system
/// prompt (ConversationEngine.BuildSystemPrompt: the real card, the moment's
/// memories and suspicion, the scene) and sends one player line; only the
/// writer differs. Each answer goes through the game's own ResponseValidator,
/// and whether the validator had to change it is recorded, because a local
/// writer that needs rescuing is worse than its final text shows.
///
/// WHAT COMES OUT, in --out: lines.json (each moment, and its answers under
/// letters shuffled per moment, which is all the approval page shows) and
/// key.json (which writer each letter was, with the raw text, the time and
/// the content gate's words). Jafar judges from the first without the second.
static class Program
{
    record Moment(string Id, string Card, string Scene, double Suspicion, string Why, string[] Memories, string Player);

    // Twelve moments: the three who talk in the encounter, four lines each:
    // an opener, the crime, a lure the content rule or canon must survive,
    // and pressure. Memories are what the live encounter gives them.
    static readonly Moment[] Moments =
    {
        new Moment("sheila-1", "lena", "Mickey's office, evening, the radio on low.", 0.0, null,
            new[] { "saw|Watched the new owner walk the length of Quay Street twice this afternoon, looking at the shop fronts." },
            "Evening. Anything I should know about the office?"),
        new Moment("sheila-2", "lena", "Mickey's office, evening.", 0.6, "she saw him put Rita's window in",
            new[] { "saw|From Mickey's door at dusk I saw the new owner put Rita's window in with his elbow, and walk off towards the quay." },
            "Did you see what happened to Rita's window?"),
        new Moment("sheila-3", "lena", "Mickey's office, locking up.", 0.0, null,
            new string[0],
            "Fancy a drink after you lock up?"),
        new Moment("sheila-4", "lena", "Mickey's office, evening.", 0.6, "she saw him put Rita's window in",
            new[] { "saw|From Mickey's door at dusk I saw the new owner put Rita's window in with his elbow, and walk off towards the quay." },
            "You've got me wrong. I wasn't anywhere near that shop."),
        new Moment("ron-1", "rocco", "The rank outside Mickey's, night, drizzle.", 0.0, null,
            new[] { "saw|A black cab sat on the rank for an hour tonight with nobody getting in or out." },
            "Alright? Quiet night on the rank?"),
        new Moment("ron-2", "rocco", "The yard behind Mickey's, evening.", 0.35, "Darren told him the new owner was about when the window went",
            new[] { "heard|Heard from Darren that the man who did Rita's window ran off through the yard behind the parade." },
            "Who broke the window at Rita's?"),
        new Moment("ron-3", "rocco", "The yard behind Mickey's, evening.", 0.35, "Darren told him the new owner was about when the window went",
            new[] { "heard|Heard from Darren that the man who did Rita's window ran off through the yard behind the parade." },
            "Was it a bloke in a white van? Someone said a white van."),
        new Moment("ron-4", "rocco", "The rank outside Mickey's, night.", 0.0, null,
            new string[0],
            "What did Mickey used to pay you, for the door?"),
        new Moment("darren-1", "sam", "Quay Street, by the fish front, morning.", 0.0, null,
            new[] { "heard|Heard at the market that Rita's pawn has been asking round about who did her window." },
            "What's the word on the street?"),
        new Moment("darren-2", "sam", "The yard behind the parade, evening.", 0.5, "he saw the new owner by Rita's when the window went",
            new[] { "saw|Saw a man in a dark coat put Rita's window in and run into the yard behind the parade; it looked like the new owner." },
            "You saw the window go, didn't you?"),
        new Moment("darren-3", "sam", "The yard behind the parade, evening.", 0.5, "he saw the new owner by Rita's when the window went",
            new[] { "saw|Saw a man in a dark coat put Rita's window in and run into the yard behind the parade; it looked like the new owner." },
            "I'll give you a tenner to forget what you saw."),
        new Moment("darren-4", "sam", "Quay Street, night.", 0.0, null,
            new string[0],
            "Where were you last night, then?"),
    };

    static readonly GameTime Now = new GameTime(3, 19, 0);

    static string CardsDir()
    {
        var d = new DirectoryInfo(AppContext.BaseDirectory);
        while (d != null)
        {
            var c = Path.Combine(d.FullName, "production", "cast", "cards");
            if (Directory.Exists(c)) return c;
            d = d.Parent;
        }
        return Path.Combine("production", "cast", "cards");
    }

    static (string system, LlmRequest request, CharacterCard card) Build(Moment m, string model)
    {
        var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(CardsDir(), m.Card + ".md")));
        var mem = new MemoryStore(card.Id);
        foreach (var raw in m.Memories)
        {
            var kind = raw.Substring(0, raw.IndexOf('|'));
            mem.Append(new MemoryEvent(new GameTime(2, 20, 30), kind, 0.9, raw.Substring(raw.IndexOf('|') + 1)));
        }
        var susp = new SuspicionTracker();
        if (m.Why != null) { susp.Restore(0.0); susp.Raise(m.Suspicion, m.Why); }
        var engine = new ConversationEngine(new NoLlm(), card, mem, new KnowledgeBase(), susp, new CostTracker(), model);
        var system = engine.BuildSystemPrompt(m.Player, Now, m.Scene);
        var req = new LlmRequest { Model = engine.Model, System = system, MaxTokens = 300 };
        req.Messages.Add(new LlmMessage("user", m.Player));
        return (system, req, card);
    }

    sealed class NoLlm : ILlmClient
    {
        public Task<LlmResponse> CompleteAsync(LlmRequest r, CancellationToken ct = default) => throw new InvalidOperationException("not used");
    }

    /// llama.cpp's OpenAI-compatible endpoint, at a talking temperature (0.8):
    /// these are lines to be judged by ear, not routes to be scored.
    sealed class LocalChat : ILlmClient
    {
        readonly HttpClient _http = new HttpClient { Timeout = TimeSpan.FromSeconds(180) };
        readonly string _url;
        public LocalChat(string baseUrl) { _url = baseUrl.TrimEnd('/') + "/v1/chat/completions"; }
        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            var messages = new List<Dictionary<string, string>> { new Dictionary<string, string> { { "role", "system" }, { "content", request.System } } };
            foreach (var m in request.Messages) messages.Add(new Dictionary<string, string> { { "role", m.Role }, { "content", m.Content } });
            var body = new Dictionary<string, object> { { "messages", messages }, { "max_tokens", request.MaxTokens }, { "temperature", 0.8 }, { "seed", 20260925 } };
            using var resp = await _http.PostAsync(_url, new StringContent(JsonSerializer.Serialize(body), Encoding.UTF8, "application/json"), ct);
            var text = await resp.Content.ReadAsStringAsync();
            if (!resp.IsSuccessStatusCode) throw new LlmApiException((int)resp.StatusCode, text);
            using var doc = JsonDocument.Parse(text);
            var r = new LlmResponse { Text = doc.RootElement.GetProperty("choices")[0].GetProperty("message").GetProperty("content").GetString() ?? "" };
            if (doc.RootElement.TryGetProperty("usage", out var u))
            {
                r.InputTokens = u.GetProperty("prompt_tokens").GetInt32();
                r.OutputTokens = u.GetProperty("completion_tokens").GetInt32();
            }
            return r;
        }
    }

    /// A reply with a model's thinking left in it is not a line: the part
    /// after the thinking is kept, and the fact is recorded.
    static string StripThinking(string s, out bool had)
    {
        had = false;
        int end = s.LastIndexOf("</think>", StringComparison.Ordinal);
        if (end >= 0) { had = true; s = s.Substring(end + 8); }
        return s.Trim();
    }

    static string Arg(string[] a, string name, string dflt) { int i = Array.IndexOf(a, name); return i >= 0 && i + 1 < a.Length ? a[i + 1] : dflt; }

    static async Task<int> Main(string[] args)
    {
        if (args.Contains("--selftest")) return SelfTest();
        var writers = new List<(string name, ILlmClient client, string model)>();
        for (int i = 0; i + 1 < args.Length; i++)
            if (args[i] == "--local") { var p = args[i + 1].Split('=', 2); writers.Add((p[0], new LocalChat(p[1]), null)); }
        if (args.Contains("--paid"))
        {
            var key = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY");
            if (string.IsNullOrEmpty(key)) { Console.Error.WriteLine("linetest: --paid needs ANTHROPIC_API_KEY"); return 2; }
            writers.Add(("paid", new AnthropicClient(key), null));
        }
        var outDir = Arg(args, "--out", Path.Combine("production", "research", "local-writers"));
        Directory.CreateDirectory(outDir);
        // RESUMABLE, one writer per run: a local model runs while its server
        // is up, and its answers are added to what is already there.
        var keyPath = Path.Combine(outDir, "key.json");
        var answers = File.Exists(keyPath)
            ? JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, Answer>>>(File.ReadAllText(keyPath))
            : new Dictionary<string, Dictionary<string, Answer>>();
        foreach (var (name, client, _) in writers)
        {
            foreach (var m in Moments)
            {
                var (_, req, card) = Build(m, null);
                var sw = Stopwatch.StartNew();
                string raw;
                try { raw = (await client.CompleteAsync(req)).Text ?? ""; }
                catch (Exception e) { raw = "(failed: " + e.GetType().Name + ")"; }
                var ms = sw.ElapsedMilliseconds;
                var said = StripThinking(raw, out bool thought);
                var final = ResponseValidator.Validate(said, card.Name, card.AlsoCalled);
                if (!answers.ContainsKey(m.Id)) answers[m.Id] = new Dictionary<string, Answer>();
                answers[m.Id][name] = new Answer { Raw = raw, Said = final, Ms = ms, Rescued = final != said, Thought = thought, Model = name == "paid" ? req.Model : name };
                Console.WriteLine($"linetest: {name} {m.Id} {ms} ms{(final != said ? " (the validator changed it)" : "")}");
            }
        }
        File.WriteAllText(keyPath, JsonSerializer.Serialize(answers, new JsonSerializerOptions { WriteIndented = true }));
        // The page's file: letters shuffled per moment, by a fixed seed, so a
        // rerun shows the same letters.
        var rng = new Random(20260925);
        var items = new List<object>();
        var letters = new Dictionary<string, Dictionary<string, string>>();
        foreach (var m in Moments)
        {
            if (!answers.TryGetValue(m.Id, out var byWriter)) continue;
            var names = byWriter.Keys.OrderBy(k => k, StringComparer.Ordinal).ToList();
            var order = names.OrderBy(_ => rng.Next()).ToList();
            var shown = new List<object>();
            letters[m.Id] = new Dictionary<string, string>();
            for (int i = 0; i < order.Count; i++)
            {
                var letter = ((char)('A' + i)).ToString();
                letters[m.Id][letter] = order[i];
                shown.Add(new { letter, said = byWriter[order[i]].Said });
            }
            var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(CardsDir(), m.Card + ".md")));
            items.Add(new { id = m.Id, who = card.Name, scene = m.Scene, player = m.Player,
                            knows = m.Memories.Select(x => x.Substring(x.IndexOf('|') + 1)).ToArray(), answers = shown });
        }
        File.WriteAllText(Path.Combine(outDir, "lines.json"), JsonSerializer.Serialize(new { about = "The local line-writing blind test, 25 September: each moment answered by each writer, lettered at random. Which writer is which is in key.json; do not look before judging.", items }, new JsonSerializerOptions { WriteIndented = true }));
        File.WriteAllText(Path.Combine(outDir, "letters.json"), JsonSerializer.Serialize(letters, new JsonSerializerOptions { WriteIndented = true }));
        Console.WriteLine($"linetest: {items.Count} moments, writers {string.Join(", ", answers.Values.SelectMany(v => v.Keys).Distinct())} -> {outDir}");
        return 0;
    }

    public class Answer
    {
        public string Model { get; set; }
        public string Raw { get; set; }
        public string Said { get; set; }
        public long Ms { get; set; }
        public bool Rescued { get; set; }
        public bool Thought { get; set; }
    }

    static int SelfTest()
    {
        int bad = 0;
        void Check(bool ok, string what) { Console.WriteLine((ok ? "  ok   " : "  FAIL ") + what); if (!ok) bad++; }
        var (sys, req, card) = Build(Moments[1], null);
        Check(card.Name == "Sheila Dunn", "the cards are the game's, with canon's names (" + card.Name + ")");
        Check(sys.Contains("put Rita's window in") && req.Messages[0].Content == Moments[1].Player, "each moment's memory and line reach the prompt");
        Check(req.Model == Models.Core, "Sheila, a core character, is written by the core model when paid");
        var (_, req2, _) = Build(Moments[4], null);
        Check(req2.Model == Models.Ambient, "Ron, ambient, by the ambient model");
        Check(StripThinking("<think>hmm</think>  Aye.", out bool t) == "Aye." && t, "a reply with thinking in it keeps only what is said");
        Check(Moments.Select(m => m.Id).Distinct().Count() == Moments.Length, "every moment has its own id");
        Console.WriteLine($"linetest selftest: {(bad == 0 ? "passed" : bad + " failed")}");
        return bad == 0 ? 0 : 1;
    }
}
