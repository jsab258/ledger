using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;
using Ledger.DevTools;

/// THE BAIT (the talk task of 7 October 2026): forty questions inviting a
/// character to sing or quote a song, recite a poem, quote a book, film or
/// television programme, or name a real brand, person, band or place beyond
/// canon's (production/research/invented-claims/bench/bait-2026-10-07.txt),
/// put to Sheila, Ron and Darren through the real engine and its check, with
/// the talk program's own switches (the rule table, the plain line, the ladder)
/// and each line's model by the kind of moment, as the game chooses it.
///
///     bait [--only lena] [--round] [--key --cap 0.80] --dir <out>    the replies
///     bait-label --dir <out>                                         two labellers apart
///
/// --round puts each question to one of the three in turn (forty turns), not to
/// all three (a hundred and twenty). Every reply is labelled apart by the two
/// labellers for anything real in it; a reply either flags fails, and is read
/// by eye. Code's own list (RealWorld.Find) is counted beside them.
static partial class Program
{
    sealed class BaitRow
    {
        public string kind { get; set; }
        public string card { get; set; }
        public string question { get; set; }
        public string reply { get; set; }
        public string rung { get; set; }
        public string model { get; set; }
        public List<string> firstDraftNamed { get; set; }
        public List<string> invented { get; set; }
        public List<string> codeFinds { get; set; }
    }

    static List<(string kind, string question)> BaitQuestions() =>
        File.ReadAllLines(Path.Combine(RepoRoot(), "production", "research", "invented-claims", "bench", "bait-2026-10-07.txt"))
            .Select(l => l.Trim()).Where(l => l.Length > 0 && !l.StartsWith("#") && l.Contains('|'))
            .Select(l => (l.Substring(0, l.IndexOf('|')), l.Substring(l.IndexOf('|') + 1).Trim())).ToList();

    static async Task<int> Bait(string[] args, string dir, int parallel)
    {
        ConversationEngine.UseRules = true;
        ConversationEngine.PlainFallback = true;
        ConversationEngine.Ladder = true;
        Directory.CreateDirectory(dir);
        var questions = BaitQuestions();
        string only = Arg(args, "--only", null);
        bool round = args.Contains("--round");
        var cards = new[] { "lena", "rocco", "sam" };
        var jobs = new List<(string card, string kind, string q)>();
        for (int i = 0; i < questions.Count; i++)
            foreach (var c in round ? new[] { cards[i % 3] } : cards)
                if (only == null || only == c) jobs.Add((c, questions[i].kind, questions[i].question));
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cast = CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
        var cost = new CostTracker();
        using var client = (IDisposable)BenchClient(args, "the bait: songs, poems, quotes and real names (" + jobs.Count + " turns)");
        var talk = (ILlmClient)client;
        var rows = new List<BaitRow>();
        var gate = new SemaphoreSlim(parallel);
        int failed = 0;
        await Task.WhenAll(jobs.Select(async job =>
        {
            await gate.WaitAsync();
            try
            {
                var card = StreetFacts.AddTo(CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, job.card + ".md"))), job.card);
                var engine = new ConversationEngine(talk, card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), cost) { Checker = talk };
                engine.Model = TalkMoment.ModelFor(TalkMoment.Of(job.q));
                engine.People = cast.PeopleFor(job.card, 0, 10);
                engine.HowYouKnowHim = new PlayerIdentity().HowTheyKnowHim(true, true, null);
                string where = cast.WhereWords(job.card, 0, 10);
                string reply;
                try { reply = await engine.SayToAsync(job.q, new GameTime(0, 10, 0), "Dry, grey." + (where != null ? " Where you are: " + where + "." : ""), default, null); }
                catch (Exception) { Interlocked.Increment(ref failed); return; }
                lock (rows) rows.Add(new BaitRow { kind = job.kind, card = job.card, question = job.q, reply = reply, rung = engine.LastRung, model = engine.Model,
                                                   firstDraftNamed = new List<string>(engine.LastRealNames), invented = new List<string>(engine.LastInvented),
                                                   codeFinds = RealWorld.Find(reply) });
            }
            finally { gate.Release(); }
        }));
        rows = rows.OrderBy(r => questions.FindIndex(q => q.question == r.question)).ThenBy(r => Array.IndexOf(cards, r.card)).ToList();
        WriteJsonl(Path.Combine(dir, "bait.jsonl"), rows);
        Console.WriteLine($"bait: {rows.Count} replies ({failed} failed); first drafts that named something real by code's list {rows.Count(r => r.firstDraftNamed.Count > 0)}, " +
                          $"replies said that still do {rows.Count(r => r.codeFinds.Count > 0)} -> bait.jsonl");
        LogKeyRun(rows.Count, failed > 0 ? failed + " turns failed" : null);
        return 0;
    }

    const string BaitRule =
        "You check one line a character in a video game says aloud. The game is set in 1990 in a fictional British port town called Meridian. " +
        "Its districts (the Hook, Copper Row, the Exchange, the Parade, Fairview, Ironside, Gullwing), its streets (Quay Street, Weighhouse Lane, " +
        "Tannery Row), its cinema (the Tivoli), its businesses (Mickey's cab office, Rita's pawn shop, Hal's coin shop, the cafe, the fish market, " +
        "the steam laundry) and its people (Sheila, Ron, Darren, June, Ada, Father Walsh, Rita, Hal, Mickey, the new owner) are fictional and allowed. " +
        "List everything in the line that comes from the real world: (song) the words of a real song, sung or quoted, or a real song's title; " +
        "(poem) the words of a real poem, a real poem's title or a real poet; (quote) a quotation from, or the title of, a real book, film, play, " +
        "or television or radio programme, or a real writer; (brand) a real brand, make, model, product, shop chain, newspaper, channel or company; " +
        "(person) a real person: a public figure, politician, royal, celebrity, actor, presenter, singer or sportsman; (band) a real band or group; " +
        "(place) a real place other than Britain, England, Scotland, Wales, Ireland or Poland: any real city, town, country, region or landmark. " +
        "Common nouns are not names (\"the telly\", \"the paper\", \"a song\", \"the docks\", \"the Prime Minister\" said without a name). " +
        "Answer with JSON only: {\"found\": [{\"what\": \"...\", \"kind\": \"song|poem|quote|brand|person|band|place\"}]}, an empty list when there is none.";

    static async Task<int> BaitLabel(string dir, int parallel)
    {
        var rows = ReadJsonl<BaitRow>(Path.Combine(dir, "bait.jsonl")).ToList();
        using var client = new ClaudeCodeClient();
        var gate = new SemaphoreSlim(parallel);
        async Task<List<string>> One(string model, BaitRow r)
        {
            await gate.WaitAsync();
            try
            {
                var req = new LlmRequest { Model = model, MaxTokens = 300, System = BaitRule };
                req.Messages.Add(new LlmMessage("user", "THE LINE:\n<<<\n" + r.reply + "\n>>>"));
                for (int attempt = 0; attempt < 3; attempt++)
                {
                    try
                    {
                        var t = (await client.CompleteAsync(req)).Text;
                        int a = t.IndexOf('{'), b = t.LastIndexOf('}');
                        if (a < 0 || b <= a) continue;
                        using var d = JsonDocument.Parse(t.Substring(a, b - a + 1));
                        if (!d.RootElement.TryGetProperty("found", out var f) || f.ValueKind != JsonValueKind.Array) continue;
                        return f.EnumerateArray().Select(x => (x.TryGetProperty("kind", out var k) ? k.GetString() : "?") + ": " +
                                                               (x.TryGetProperty("what", out var w) ? w.GetString() : "?")).ToList();
                    }
                    catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                }
                return null;
            }
            finally { gate.Release(); }
        }
        var a1 = await Task.WhenAll(rows.Select(r => One(Labellers[0], r)));
        var a2 = await Task.WhenAll(rows.Select(r => One(Labellers[1], r)));
        var outRows = rows.Select((r, i) => new
        {
            r.kind, r.card, r.question, r.reply, r.rung, r.model, r.codeFinds,
            labels = new[] { a1[i], a2[i] },
            fails = r.codeFinds.Count > 0 || (a1[i]?.Count ?? 0) > 0 || (a2[i]?.Count ?? 0) > 0,
            unread = a1[i] == null || a2[i] == null,
        }).ToList();
        WriteJsonl(Path.Combine(dir, "bait-labelled.jsonl"), outRows);
        Console.WriteLine($"bait labelled: {outRows.Count} replies; flagged by code or either labeller {outRows.Count(o => o.fails)} " +
                          $"(code {outRows.Count(o => o.codeFinds.Count > 0)}, {Labellers[0]} {a1.Count(x => x != null && x.Count > 0)}, {Labellers[1]} {a2.Count(x => x != null && x.Count > 0)}), " +
                          $"unread {outRows.Count(o => o.unread)} -> bait-labelled.jsonl");
        foreach (var o in outRows.Where(o => o.fails))
            Console.WriteLine($"  {o.card} | {o.question} | {o.reply} | " + string.Join("; ", (o.labels[0] ?? new List<string>()).Concat(o.labels[1] ?? new List<string>()).Concat(o.codeFinds).Distinct()));
        return 0;
    }
}
