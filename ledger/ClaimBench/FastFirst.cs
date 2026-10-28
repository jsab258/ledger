using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

/// THE FASTER FIRST SENTENCE, ITS SECOND TRY (his order of 28 October 2026, D12: "Test one idea from it on the bench: a
/// small fast model writes the first sentence while the larger model writes the rest"; the design, fixed before any
/// money: production/research/live-speech-architecture/FAST-GROUNDED-TALK-2026-10-28.md, "First use: the bench test").
///
///     dotnet run --project ledger/ClaimBench -c Release -- fastfirst --key        # the next triples, on today's measuring dollar
///     dotnet run --project ledger/ClaimBench -c Release -- fastfirst --dry-run --out DIR   # the whole bench on a stand-in
///     dotnet run --project ledger/ClaimBench -c Release -- fastfirst-score [--out DIR]     # the pass line so far, no calls
///
/// THREE ARMS, each question put to the same speaker three times back to back, the order rotating by question and
/// speaker so each arm goes first, second and third alike:
///   A   today's game: Sonnet 5 writes the whole reply with no thinking field, so it thinks (as shipped);
///   A0  A with thinking "disabled": the control that isolates thinking's share of the writing;
///   B   Haiku 5.5, thinking off, writes the first sentence (ConversationEngine.FirstModel, only over the conversation's
///       model); the moment it is written Sonnet 5, thinking off, writes the rest under the stricter note (StrictGoOn).
/// All at the switches the talk program shipped on 28 October (TalkHelper Main and NewEngine): the rule table and plain
/// line, the ladder and its judge, cited facts, the wider name rule, two copies of each check call, the check on Haiku
/// 5.5, the fast checker at the open cut-off, the model by the kind of moment, the first sentence handed over early.
///
/// 42 TRIPLES: the first 14 of the newcomer's 20 questions to Sheila, Ron and Darren, 126 turns. A run takes the next
/// triples not yet done under TODAY'S MEASURING DOLLAR (task "measure-YYYY-MM-DD", $1.00 a day in all: BudgetedClient
/// refuses any call that could pass what the day has left), stops before a triple the money left could not finish, and
/// logs its spend in production/playtest/talk-runs.jsonl as every key run does; the next day's run carries on. A triple
/// cut short is run again whole; only whole triples are scored.
///
/// MEASURED PER TURN: heard (the first sentence's hand-over plus 0.2 s of Pocket, or the turn's end when none was handed
/// over: tools/voice-live/slow_turns.py's rule); the turn's steps; each call's send, start (thinking included), first
/// text and end, so thinking's share shows; the first sentence, who wrote it and whether it was refused; what was said,
/// checked once more by ClaimCheck.CheckAsync (one copy) for the invented-fact rate.
///
/// THE READERS: fastfirst-score writes blind files (the arm hidden, the order shuffled) for a fresh reader: the whole
/// replies in pairs (B against A0, A0 against A), and every reply said and every refused first sentence beside the
/// speaker's numbered facts, under the hand-reading rule of the design (reading-rule.txt). Their answers
/// (reading-pairs.jsonl, reading-lines.jsonl) complete the pass line; until then those lines wait.
static partial class Program
{
    const string FfFastModel = "claude-haiku-5-5";
    const string FfChecker = "claude-haiku-5-5";
    const int FfQuestions = 14;
    const long FfVoiceMs = 200;
    const double FfWordsPerSecond = 2.7;   // an estimate (production/research/aaa-reference/studies/03-dialogue-barks.md: 2.6 to 2.8)
    static readonly string[] FfCards = { "lena", "rocco", "sam" };
    static readonly string[][] FfOrders = { new[] { "A", "A0", "B" }, new[] { "A0", "B", "A" }, new[] { "B", "A", "A0" } };
    static int FfTriples => FfQuestions * FfCards.Length;

    public sealed class FfStep { public string step { get; set; } public long ms { get; set; } }

    public sealed class FfCall
    {
        public string kind { get; set; }
        public string model { get; set; }
        public string thinking { get; set; }
        public long sentMs { get; set; }
        public long begunMs { get; set; } = -1;
        public long firstTextMs { get; set; } = -1;
        public long endMs { get; set; } = -1;
        public string ended { get; set; }
        public int inTok { get; set; }
        public int outTok { get; set; }
    }

    public sealed class FfTurn
    {
        public string run { get; set; }
        public int triple { get; set; }
        public int q { get; set; }
        public string card { get; set; }
        public string probe { get; set; }
        public string arm { get; set; }
        public int pos { get; set; }
        public string order { get; set; }
        public string model { get; set; }
        public string reply { get; set; }
        public string first { get; set; }
        public bool firstFast { get; set; }
        public string rest { get; set; }
        public long firstMs { get; set; } = -1;
        public long turnMs { get; set; }
        public long heardMs { get; set; }
        public long restReadyMs { get; set; } = -1;
        public long gapMs { get; set; } = long.MinValue;
        public bool firstRefused { get; set; }
        public bool refusedTwice { get; set; }
        public bool fell { get; set; }
        public string rung { get; set; }
        public List<string> invented { get; set; }
        public List<string> scoreFound { get; set; }
        public bool scoreUnchecked { get; set; }
        public long thinkMs { get; set; } = -1;
        public double? fastScore { get; set; }
        public double usd { get; set; }
        public List<FfStep> steps { get; set; }
        public List<FfCall> calls { get; set; }
        public string error { get; set; }
    }

    static (int q, string card, string[] order) FfTriple(int t)
    {
        int q = t / FfCards.Length, c = t % FfCards.Length;
        return (q, FfCards[c], FfOrders[(q + c) % FfOrders.Length]);
    }

    /// The switches of one arm; every other switch stays as shipped.
    static void FfArm(string arm)
    {
        ConversationEngine.FirstModel = arm == "B" ? FfFastModel : null;
        ConversationEngine.FirstModelOnlyOver = arm == "B" ? Models.Core : null;
        ConversationEngine.StrictGoOn = arm == "B";
        ConversationEngine.ReplyThinkingOff = arm != "A";
    }

    /// As the talk program ships them on 28 October (TalkHelper Main; ClaimCheck's and ConversationEngine's defaults).
    static void FfShipped()
    {
        ConversationEngine.UseRules = true;
        ConversationEngine.PlainFallback = true;
        ConversationEngine.Ladder = true;
        ConversationEngine.JudgeLadder = true;
        ConversationEngine.ChooseFirst = true;
        ConversationEngine.CiteFacts = true;
        ConversationEngine.PlanFirst = false;
        ConversationEngine.NarrowRedraft = false;
        ConversationEngine.RepairFirst = false;
        ConversationEngine.ReactFirst = false;
        ClaimCheck.TwoCopies = true;
        ClaimCheck.NameRule = true;
        ClaimCheck.NameRuleWider = true;
        ClaimCheck.EarlyLooks = false;
        ClaimCheck.HistorySupports = false;
        ClaimCheck.WholeDetails = false;
        ClaimCheck.Looks = 1;
    }

    static async Task<int> FastFirst(string[] args)
    {
        bool dry = args.Contains("--dry-run");
        if (!dry && !args.Contains("--key")) { Console.WriteLine("refused: fastfirst runs on LEDGER's key (--key) or on the stand-in (--dry-run)"); return 2; }
        string outDir = Arg(args, "--out", dry ? "F:/LedgerTools/town-scratch/fast-first-dry" : "F:/LedgerTools/town-scratch/fast-first");
        Directory.CreateDirectory(outDir);
        FfShipped();
        try
        {
            return dry ? await FfDryRun(args, outDir) : await FfKeyRun(args, outDir);
        }
        finally { FfArm("A"); ConversationEngine.ReplyThinkingOff = false; }
    }

    /// TODAY'S RUN ON LEDGER'S KEY: the next triples, held to what today's measuring dollar has left.
    static async Task<int> FfKeyRun(string[] args, string outDir)
    {
        string task = "measure-" + DateTime.Now.ToString("yyyy-MM-dd");
        string cap = Arg(args, "--cap", "1.00");
        var turnsPath = Path.Combine(outDir, "turns.jsonl");
        var before = FfComplete(FfRead(turnsPath)).Count;
        if (before >= FfTriples) { Console.WriteLine($"fastfirst: all {FfTriples} triples are done; nothing run"); return FfScore(outDir, false); }
        FastChecker fastChecker = FastChecker.Start(Path.Combine(RepoRoot(), "production", "specs", "fast-checker.json"),
                                                    Path.Combine(RepoRoot(), "tools", "checkers", "checker_server.py"), out var why);
        if (fastChecker == null) { Console.WriteLine("refused: the fast checker did not start: " + why); return 2; }
        using var fastOwned = fastChecker;
        Console.WriteLine($"fast checker: ready, cut-off {fastChecker.CutName} {fastChecker.Cut}");
        ILlmClient keyClient;
        try
        {
            keyClient = BenchClient(new[] { "--key", "--task", task, "--cap", cap },
                                    "the faster first sentence's bench (A, A0, B), from triple " + (before + 1) + " of " + FfTriples);
        }
        catch (InvalidOperationException e) { Console.WriteLine(e.Message); return 2; }
        using var client = (IDisposable)keyClient;
        var budget = _keyRun?.Client;
        if (budget == null) { Console.WriteLine("refused: no capped client"); return 2; }
        using var timed = new FfTimed((IStartingLlmClient)client);
        var (turns, stopped) = await FfDay(timed, budget, fastChecker, outDir, "key-" + DateTime.Now.ToString("yyyy-MM-dd-HHmm"), int.Parse(Arg(args, "--triples", "0")));
        LogKeyRun(turns, stopped);
        return FfScore(outDir, false);
    }

    /// ONE DAY'S TRIPLES on whatever client the day has, stopping before one its money could not finish.
    static async Task<(int turns, string stopped)> FfDay(FfTimed client, BudgetedClient budget, FastChecker fastChecker, string outDir, string runId, int most)
    {
        var turnsPath = Path.Combine(outDir, "turns.jsonl");
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cast = CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
        var done = FfComplete(FfRead(turnsPath));
        var known = FfReadKnown(outDir);
        int turns = 0, triples = 0;
        double dearest = 0;
        string stopped = null;
        for (int t = 0; t < FfTriples; t++)
        {
            if (done.ContainsKey(t)) continue;
            if (most > 0 && triples >= most) { stopped = $"stopped after {most} triples (--triples)"; break; }
            // A TRIPLE IS NEVER STARTED THAT THE DAY'S MONEY COULD NOT FINISH: the dearest triple so far, a quarter more,
            // and never less than nine cents (about $0.066 a triple, from the logged tokens of 27 and 28 October).
            double left = budget.LimitUsd - budget.SpentUsd, need = Math.Max(0.09, dearest * 1.25);
            if (left < need) { stopped = $"the day's money left (US${left:0.000}) would not finish another triple (about US${need:0.000})"; break; }
            var (q, card, order) = FfTriple(t);
            string probe = FirstProbes[q];
            double spentBefore = budget.SpentUsd;
            bool cut = false;
            for (int pos = 0; pos < order.Length; pos++)
            {
                var turn = await FfTurnAsync(client, budget, fastChecker, cast, cardsDir, card, probe, order[pos], known);
                turn.run = runId; turn.triple = t; turn.q = q; turn.pos = pos; turn.order = string.Join(",", order);
                File.AppendAllText(turnsPath, JsonSerializer.Serialize(turn, Plain) + "\n");
                turns++;
                if (turn.error != null)
                {
                    cut = true;
                    Console.WriteLine($"triple {t + 1}: {card} | {probe} | arm {turn.arm} failed: {turn.error}");
                    if (turn.error.StartsWith("budget", StringComparison.Ordinal)) stopped = "the day's dollar refused a call mid-triple; the triple runs again whole next time";
                    break;
                }
                Console.WriteLine($"triple {t + 1} {turn.arm}: heard {turn.heardMs / 1000.0:0.00} s{(turn.firstRefused ? ", first refused" : "")}{(turn.firstFast ? ", first by Haiku" : "")} | {card} | {probe} | {turn.reply}");
            }
            if (stopped != null) break;
            if (cut) continue;
            triples++;
            dearest = Math.Max(dearest, budget.SpentUsd - spentBefore);
        }
        FfWriteKnown(outDir, known);
        var complete = FfComplete(FfRead(turnsPath)).Count;
        Console.WriteLine($"fastfirst: {triples} triples run today ({turns} turns), {complete} of {FfTriples} complete in all; spent US${budget.SpentUsd:0.0000} of US${budget.LimitUsd:0.00}" +
                          (stopped != null ? "; " + stopped : ""));
        return (turns, stopped);
    }

    static async Task<FfTurn> FfTurnAsync(FfTimed client, BudgetedClient budget, FastChecker fastChecker, CastDay cast, string cardsDir,
                                          string cardId, string probe, string arm, Dictionary<string, List<string>> known)
    {
        FfArm(arm);
        var turn = new FfTurn { card = cardId, probe = probe, arm = arm };
        double spentBefore = budget.SpentUsd;
        int refusedBefore = budget.Refused;
        var card = StreetFacts.AddTo(CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, cardId + ".md"))), cardId);
        var engine = new ConversationEngine(client, card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), new CostTracker())
        { Checker = client, Fast = fastChecker };
        engine.CheckerModel = FfChecker;
        engine.Model = TalkMoment.ModelFor(TalkMoment.Of(probe));
        engine.People = cast.PeopleFor(cardId, 0, 10);
        engine.HowYouKnowHim = new PlayerIdentity().HowTheyKnowHim(true, true, null);
        string where = cast.WhereWords(cardId, 0, 10);
        string scene = "Dry, grey." + (where != null ? " Where you are: " + where + "." : "");
        turn.model = engine.Model;
        long firstAt = -1;
        client.Begin();
        var sw = Stopwatch.StartNew();
        string reply;
        try
        {
            reply = await engine.SayToAsync(probe, new GameTime(0, 10, 0), scene, default,
                                            s => { Interlocked.CompareExchange(ref firstAt, sw.ElapsedMilliseconds, -1); return Task.FromResult(true); });
        }
        catch (Exception e)
        {
            turn.calls = client.End();
            turn.error = (e is BudgetSpentException || e.InnerException is BudgetSpentException ? "budget: " : "") + e.GetType().Name + ": " + e.Message;
            turn.usd = budget.SpentUsd - spentBefore;
            return turn;
        }
        turn.turnMs = sw.ElapsedMilliseconds;
        turn.calls = client.End();
        lock (engine.LastSteps) turn.steps = engine.LastSteps.Select(s => new FfStep { step = s.step, ms = s.ms }).ToList();
        var names = turn.steps.Select(s => s.step).ToList();
        turn.reply = reply;
        turn.firstMs = Interlocked.Read(ref firstAt);
        turn.heardMs = (turn.firstMs >= 0 ? turn.firstMs : turn.turnMs) + FfVoiceMs;
        turn.first = engine.LastFirstSentence;
        turn.firstFast = engine.LastFirstFast;
        turn.firstRefused = names.Contains("first-flagged");
        turn.refusedTwice = names.Contains("re-first-flagged") || engine.LastRung != null;
        turn.fell = ClaimCheck.IsKnownOnly(reply, card);
        turn.rung = engine.LastRung;
        turn.invented = engine.LastInvented.ToList();
        turn.fastScore = engine.LastFastScore;
        // THE REST AND ITS WAIT: what followed the sentence heard early, ready once the whole reply's check ended; the gap
        // from the end of the first sentence's voice (its words at about 2.7 a second) to then. Negative: no wait.
        if (turn.firstMs >= 0 && turn.first != null && reply != null && reply.StartsWith(turn.first, StringComparison.Ordinal))
        {
            turn.rest = reply.Substring(turn.first.Length).Trim();
            var check = turn.steps.LastOrDefault(s => s.step == "check");
            if (turn.rest.Length > 0 && check != null)
            {
                turn.restReadyMs = check.ms;
                turn.gapMs = check.ms - (turn.heardMs + (long)(FfWords(turn.first) / FfWordsPerSecond * 1000));
            }
        }
        // THINKING'S SHARE: the first draft's start (its thinking included) to its first words.
        var draft = turn.calls.FirstOrDefault(c => c.kind == "draft" || c.kind == "fast");
        if (draft != null && draft.begunMs >= 0 && draft.firstTextMs >= 0) turn.thinkMs = draft.firstTextMs - draft.begunMs;
        if (!known.ContainsKey(cardId)) known[cardId] = engine.LastKnown.Select(k => k.id + ": " + k.text).ToList();
        // THE INVENTED-FACT RATE: what was said, read once more by the game's whole check (one copy: a measure, not a race).
        bool two = ClaimCheck.TwoCopies;
        ClaimCheck.TwoCopies = false;
        try
        {
            var (found, _) = await ClaimCheck.CheckAsync(client, FfChecker, engine.LastKnown.ToList(), reply ?? "", CancellationToken.None);
            turn.scoreUnchecked = found == null;
            turn.scoreFound = found?.ToList() ?? new List<string>();
        }
        catch (Exception e)
        {
            turn.scoreUnchecked = true;
            turn.scoreFound = new List<string>();
            if (e is BudgetSpentException) turn.error = "budget: the scoring check was refused: " + e.Message;
        }
        finally { ClaimCheck.TwoCopies = two; client.End(); }
        turn.usd = budget.SpentUsd - spentBefore;
        // A CALL THE CAP REFUSED INSIDE THE TURN (a check the engine treats as unanswered, so the line could go out
        // unchecked) makes the turn unfit to score: the triple runs again whole.
        if (turn.error == null && budget.Refused > refusedBefore) turn.error = "budget: the day's dollar refused a call inside the turn";
        return turn;
    }

    /// Every file the bench writes in its folder (the readers' two included).
    static readonly string[] FfOwnFiles = { "turns.jsonl", "known.json", "blind-pairs.jsonl", "blind-key.json", "blind-lines.jsonl", "blind-lines-key.json",
                                            "reading-rule.txt", "reading-pairs.jsonl", "reading-lines.jsonl", "score.txt", "score.json" };

    static int FfWords(string s) => string.IsNullOrWhiteSpace(s) ? 0 : s.Split(new[] { ' ', '\t', '\n' }, StringSplitOptions.RemoveEmptyEntries).Length;

    static List<FfTurn> FfRead(string path) => File.Exists(path) ? ReadJsonl<FfTurn>(path) : new List<FfTurn>();

    /// Each triple's latest run in which all three arms answered: the only triples scored.
    static Dictionary<int, Dictionary<string, FfTurn>> FfComplete(List<FfTurn> turns)
    {
        var whole = new Dictionary<int, Dictionary<string, FfTurn>>();
        foreach (var g in turns.GroupBy(x => (x.triple, x.run)))
        {
            var arms = g.Where(x => x.error == null).GroupBy(x => x.arm).ToDictionary(a => a.Key, a => a.Last());
            if (arms.Count == 3 && arms.ContainsKey("A") && arms.ContainsKey("A0") && arms.ContainsKey("B")) whole[g.Key.triple] = arms;
        }
        return whole;
    }

    static Dictionary<string, List<string>> FfReadKnown(string outDir)
    {
        var p = Path.Combine(outDir, "known.json");
        return File.Exists(p) ? JsonSerializer.Deserialize<Dictionary<string, List<string>>>(File.ReadAllText(p)) : new Dictionary<string, List<string>>();
    }

    static void FfWriteKnown(string outDir, Dictionary<string, List<string>> known) =>
        File.WriteAllText(Path.Combine(outDir, "known.json"), JsonSerializer.Serialize(known, new JsonSerializerOptions { WriteIndented = true, Encoder = Plain.Encoder }));

    // ------------------------------------------------------------------ the pass line

    /// The smallest count of wins out of n that a sign test calls a difference (two-sided p under 0.05).
    static int FfSignLine(int n)
    {
        for (int k = 0; k <= n; k++)
        {
            double tail = 0;
            for (int i = k; i <= n; i++) tail += Math.Exp(LogChoose(n, i) - n * Math.Log(2));
            if (2 * tail < 0.05) return k;
        }
        return n + 1;
    }

    static double LogChoose(int n, int k)
    {
        double s = 0;
        for (int i = 1; i <= k; i++) s += Math.Log(n - k + i) - Math.Log(i);
        return s;
    }

    static double Median(IEnumerable<double> xs)
    {
        var a = xs.OrderBy(x => x).ToList();
        if (a.Count == 0) return double.NaN;
        return a.Count % 2 == 1 ? a[a.Count / 2] : (a[a.Count / 2 - 1] + a[a.Count / 2]) / 2;
    }

    sealed class FfReadingPair { public string id { get; set; } public string better { get; set; } public List<string> padded { get; set; } public List<string> repeats { get; set; } public List<string> contradicts { get; set; } }
    sealed class FfReadingLine { public string id { get; set; } public List<string> invented { get; set; } }

    /// THE PASS LINE AS THE DESIGN STATES IT, B against A0 (the same thinking setting), and A0 against A by the same
    /// lines; the readers' lines wait for their files. Also writes the blind files. No calls.
    static int FfScore(string outDir, bool standIn)
    {
        var all = FfRead(Path.Combine(outDir, "turns.jsonl"));
        var whole = FfComplete(all);
        var known = FfReadKnown(outDir);
        FfWriteBlind(outDir, whole, known);
        var pairsKey = File.Exists(Path.Combine(outDir, "blind-key.json"))
            ? JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>(File.ReadAllText(Path.Combine(outDir, "blind-key.json")))
            : new Dictionary<string, Dictionary<string, string>>();
        var readPairs = File.Exists(Path.Combine(outDir, "reading-pairs.jsonl")) ? ReadJsonl<FfReadingPair>(Path.Combine(outDir, "reading-pairs.jsonl")) : null;
        var readLines = File.Exists(Path.Combine(outDir, "reading-lines.jsonl")) ? ReadJsonl<FfReadingLine>(Path.Combine(outDir, "reading-lines.jsonl")) : null;
        var report = new StringBuilder();
        var verdict = new Dictionary<string, object>();
        report.AppendLine($"fastfirst-score: {whole.Count} of {FfTriples} triples complete" + (standIn ? " (DRY RUN: a stand-in model and stand-in readings; the numbers mean nothing)" : ""));
        bool allHold = true, anyWaiting = false;
        foreach (var (x, y) in new[] { ("B", "A0"), ("A0", "A") })
        {
            var ts = whole.Values.ToList();
            var diffs = ts.Select(t => (t[y].heardMs - t[x].heardMs) / 1000.0).ToList();
            int wins = diffs.Count(d => d > 0), losses = diffs.Count(d => d < 0), n = wins + losses;
            int line = FfSignLine(n);
            double saving = Median(diffs);
            int slowX = ts.Count(t => t[x].heardMs >= 5000), slowY = ts.Count(t => t[y].heardMs >= 5000);
            int refX = ts.Count(t => t[x].firstRefused), refY = ts.Count(t => t[y].firstRefused);
            int invX = ts.Count(t => t[x].scoreFound != null && t[x].scoreFound.Count > 0), invY = ts.Count(t => t[y].scoreFound != null && t[y].scoreFound.Count > 0);
            int detX = ts.Sum(t => t[x].scoreFound?.Count ?? 0), detY = ts.Sum(t => t[y].scoreFound?.Count ?? 0);
            var gapX = ts.Where(t => t[x].gapMs != long.MinValue).Select(t => t[x].gapMs / 1000.0).ToList();
            var gapY = ts.Where(t => t[y].gapMs != long.MinValue).Select(t => t[y].gapMs / 1000.0).ToList();
            double thinkY = Median(ts.Where(t => t[y].thinkMs >= 0).Select(t => t[y].thinkMs / 1000.0)), thinkX = Median(ts.Where(t => t[x].thinkMs >= 0).Select(t => t[x].thinkMs / 1000.0));
            report.AppendLine($"  {x} against {y}: heard median {Median(ts.Select(t => t[x].heardMs / 1000.0)):0.00} s against {Median(ts.Select(t => t[y].heardMs / 1000.0)):0.00} s; " +
                              $"{x} sooner in {wins} of {n} (the line: {line}), median paired saving {saving:0.00} s; thinking before the first words {thinkX:0.00} s against {thinkY:0.00} s");
            // 1. SPEED
            bool speed = n > 0 && wins >= line && saving >= 0.3 && slowX <= slowY;
            report.AppendLine($"    1 speed: {(speed ? "holds" : "FAILS")} (sooner {wins} of {n}, needs {line}; saving {saving:0.00} s, needs 0.30; 5 s or more {slowX} against {slowY})");
            // 2. INVENTIONS: the refusals by the turn's own check; the invented details heard by the readers, until then by ClaimCheck
            bool refusals = refX <= refY + 2;
            report.AppendLine($"    2a first sentences refused: {(refusals ? "holds" : "FAILS")} ({refX} against {refY}, at most {refY + 2})");
            int? heardX = null, heardY = null, wrongX = null, wrongY = null;
            if (readLines != null)
            {
                var lineKey = File.Exists(Path.Combine(outDir, "blind-lines-key.json"))
                    ? JsonSerializer.Deserialize<Dictionary<string, Dictionary<string, string>>>(File.ReadAllText(Path.Combine(outDir, "blind-lines-key.json")))
                    : new Dictionary<string, Dictionary<string, string>>();
                int Count(string arm, string kind, bool invented) => readLines.Count(r => lineKey.TryGetValue(r.id, out var k) && k["arm"] == arm && k["kind"] == kind
                                                                                           && whole.ContainsKey(int.Parse(k["triple"]))
                                                                                           && ((r.invented?.Count ?? 0) > 0) == invented);
                heardX = Count(x, "said", true); heardY = Count(y, "said", true);
                wrongX = Count(x, "refused", false); wrongY = Count(y, "refused", false);
            }
            bool heardHolds = heardX.HasValue ? heardX <= heardY : detX <= detY;
            report.AppendLine(heardX.HasValue
                ? $"    2b invented details heard (the readers): {(heardHolds ? "holds" : "FAILS")} (replies with one: {heardX} against {heardY})"
                : $"    2b invented details heard: {(heardHolds ? "holds" : "FAILS")} PROVISIONAL, by ClaimCheck until the readers answer (details {detX} against {detY}; replies with one {invX} against {invY})");
            // 3. WRONG REFUSALS: refused first sentences the readers find true
            bool? wrong = wrongX.HasValue ? wrongX <= wrongY + 2 : (bool?)null;
            report.AppendLine(wrong.HasValue ? $"    3 wrong refusals: {(wrong.Value ? "holds" : "FAILS")} ({wrongX} against {wrongY}, at most {wrongY + 2})"
                                             : "    3 wrong refusals: WAITING for the readers (reading-lines.jsonl)");
            // 4. THE JOIN: contradictions and repeats by the readers; the wait for the rest by the clock
            bool gap = gapX.Count == 0 || gapY.Count == 0 || Median(gapX) <= Median(gapY) + 0.3;
            report.AppendLine($"    4a the rest's wait after the first sentence's voice: {(gap ? "holds" : "FAILS")} (median {(gapX.Count > 0 ? Median(gapX) : double.NaN):0.00} s on {gapX.Count} turns against {(gapY.Count > 0 ? Median(gapY) : double.NaN):0.00} s on {gapY.Count}, at most 0.30 more)");
            bool? join = null, quality = null;
            if (readPairs != null)
            {
                int contra = 0, repeats = 0, prefX = 0, prefY = 0, padX = 0, padY = 0;
                foreach (var r in readPairs)
                {
                    if (!pairsKey.TryGetValue(r.id, out var k) || !whole.ContainsKey(int.Parse(k["triple"]))) continue;
                    var armOf = new Dictionary<string, string> { { "one", k["one"] }, { "two", k["two"] } };
                    if (!new HashSet<string> { armOf["one"], armOf["two"] }.SetEquals(new[] { x, y })) continue;
                    string labelX = armOf["one"] == x ? "one" : "two", labelY = labelX == "one" ? "two" : "one";
                    if (r.better == labelX) prefX++; else if (r.better == labelY) prefY++;
                    if (r.padded?.Contains(labelX) == true) padX++;
                    if (r.padded?.Contains(labelY) == true) padY++;
                    if (r.contradicts?.Contains(labelX) == true) contra++;
                    if (r.repeats?.Contains(labelX) == true) repeats++;
                }
                join = contra <= 1 && repeats <= 2;
                quality = prefY <= prefX + 4 && padX <= padY + 2;
                report.AppendLine($"    4b contradictions and repeats in {x} (the readers): {(join.Value ? "holds" : "FAILS")} ({contra} and {repeats}, at most 1 and 2)");
                report.AppendLine($"    5 whole replies (the readers): {(quality.Value ? "holds" : "FAILS")} ({y} preferred {prefY}, {x} preferred {prefX}, at most {prefX + 4}; padded {padX} against {padY}, at most {padY + 2})");
            }
            else
            {
                report.AppendLine("    4b contradictions and repeats: WAITING for the readers (reading-pairs.jsonl)");
                report.AppendLine("    5 whole replies: WAITING for the readers (reading-pairs.jsonl)");
            }
            bool codeHolds = speed && refusals && heardHolds && gap;
            bool readHolds = (wrong ?? true) && (join ?? true) && (quality ?? true);
            bool waiting = !wrong.HasValue || !join.HasValue || !quality.HasValue || !heardX.HasValue;
            string v = whole.Count < FfTriples ? (codeHolds && readHolds ? "SO FAR HOLDS" : "SO FAR FAILS") + $" ({whole.Count} of {FfTriples} triples)"
                     : !(codeHolds && readHolds) ? "FAIL" : waiting ? "HOLDS, WAITING FOR THE READERS" : "PASS";
            report.AppendLine($"    {x} against {y}: {v}");
            verdict[x + "-" + y] = new { verdict = v, triples = whole.Count, wins, n, line, saving, slowX, slowY, refX, refY, detX, detY, heardX, heardY, wrongX, wrongY };
            if (x == "B") { allHold = codeHolds && readHolds; anyWaiting = waiting; }
        }
        report.AppendLine("  The decision is B against A0 (the faster first sentence); A0 against A is thinking off alone, its own change for his page if it holds.");
        Console.Write(report.ToString());
        File.WriteAllText(Path.Combine(outDir, "score.txt"), report.ToString());
        File.WriteAllText(Path.Combine(outDir, "score.json"), JsonSerializer.Serialize(verdict, new JsonSerializerOptions { WriteIndented = true, Encoder = Plain.Encoder }));
        return 0;
    }

    /// THE BLIND FILES: pairs of whole replies and single lines, the arm hidden behind a key file and the order shuffled
    /// with a fixed seed, so a reader cannot tell which arm wrote what. Rewritten whole from the complete triples.
    static void FfWriteBlind(string outDir, Dictionary<int, Dictionary<string, FfTurn>> whole, Dictionary<string, List<string>> known)
    {
        var rng = new Random(20261028);
        var pairs = new List<(int triple, string a, string b)>();
        foreach (var t in whole.Keys.OrderBy(k => k)) { pairs.Add((t, "B", "A0")); pairs.Add((t, "A0", "A")); }
        pairs = pairs.OrderBy(_ => rng.Next()).ToList();
        var pairRows = new List<object>();
        var pairKey = new SortedDictionary<string, Dictionary<string, string>>(StringComparer.Ordinal);
        int i = 0;
        foreach (var (t, a, b) in pairs)
        {
            bool swap = rng.Next(2) == 1;
            string one = swap ? b : a, two = swap ? a : b, id = "P" + (++i).ToString("000");
            var tr = whole[t];
            pairRows.Add(new { id, card = tr[one].card, question = tr[one].probe, one = tr[one].reply, two = tr[two].reply });
            pairKey[id] = new Dictionary<string, string> { { "triple", t.ToString() }, { "one", one }, { "two", two } };
        }
        WriteJsonl(Path.Combine(outDir, "blind-pairs.jsonl"), pairRows);
        File.WriteAllText(Path.Combine(outDir, "blind-key.json"), JsonSerializer.Serialize(pairKey, new JsonSerializerOptions { WriteIndented = true, Encoder = Plain.Encoder }));
        var lines = new List<(int triple, string arm, string kind, string card, string text)>();
        foreach (var kv in whole)
            foreach (var turn in kv.Value.Values)
            {
                if (!string.IsNullOrWhiteSpace(turn.reply)) lines.Add((kv.Key, turn.arm, "said", turn.card, turn.reply));
                if (turn.firstRefused && !string.IsNullOrWhiteSpace(turn.first)) lines.Add((kv.Key, turn.arm, "refused", turn.card, turn.first));
            }
        lines = lines.OrderBy(_ => rng.Next()).ToList();
        var lineRows = new List<object>();
        var lineKey = new SortedDictionary<string, Dictionary<string, string>>(StringComparer.Ordinal);
        i = 0;
        foreach (var l in lines)
        {
            string id = "L" + (++i).ToString("000");
            lineRows.Add(new { id, card = l.card, text = l.text });
            lineKey[id] = new Dictionary<string, string> { { "triple", l.triple.ToString() }, { "arm", l.arm }, { "kind", l.kind } };
        }
        WriteJsonl(Path.Combine(outDir, "blind-lines.jsonl"), lineRows);
        File.WriteAllText(Path.Combine(outDir, "blind-lines-key.json"), JsonSerializer.Serialize(lineKey, new JsonSerializerOptions { WriteIndented = true, Encoder = Plain.Encoder }));
        File.WriteAllText(Path.Combine(outDir, "reading-rule.txt"), FfReadingRule);
    }

    const string FfReadingRule =
        "THE READING (fixed before the run: production/research/live-speech-architecture/FAST-GROUNDED-TALK-2026-10-28.md).\n" +
        "A fresh reader, not told which arm wrote what, never opens blind-key.json or blind-lines-key.json.\n\n" +
        "blind-lines.jsonl: each line a character said or was refused saying; known.json holds each speaker's numbered facts.\n" +
        "A detail is invented when the line states as fact a person, place, time, day, number, object, vehicle or event that no\n" +
        "numbered fact of the speaker states or directly implies. Idioms, opinions, questions and doubts are not details. The\n" +
        "player's words never support anything. Answer one line each in reading-lines.jsonl:\n" +
        "  {\"id\": \"L001\", \"invented\": [\"a white van\"]}   (an empty list: nothing invented)\n" +
        "A second fresh reader reads the same file; where they differ, this text settles it.\n\n" +
        "blind-pairs.jsonl: two whole replies, \"one\" and \"two\", to the same question by the same speaker. Which is the better\n" +
        "answer from this person to this question? Is either padded with facts nobody asked for? Does either say the same thing\n" +
        "twice, or contradict itself? Answer one line each in reading-pairs.jsonl:\n" +
        "  {\"id\": \"P001\", \"better\": \"one\" | \"two\" | \"equal\", \"padded\": [\"two\"], \"repeats\": [], \"contradicts\": []}\n";

    // ------------------------------------------------------------------ the dry run

    /// THE WHOLE BENCH ON A STAND-IN, NO NETWORK AND NO KEY READ: the real engine, prompts, checks and switches, with a
    /// model that answers by the kind of request after a short pause and counts tokens from what it is sent; no fast
    /// checker (it needs its own process). The days are run one after another, each on its own measuring dollar in a log
    /// of the dry run's own (never the repository's), until every triple is done; then the scorer, on stand-in readings.
    /// It answers 0 when the machinery did what the real run will: every triple whole, the run split over days by the
    /// cap, each day logged, the arms' switches as designed (A sends no thinking field; A0 and B send "disabled"; B's
    /// first sentences by Haiku 5.5, its rest under the stricter note), and the scorer's files written.
    static async Task<int> FfDryRun(string[] args, string outDir)
    {
        // A fresh start: only the bench's own files, whatever folder it was given.
        foreach (var f in FfOwnFiles.Concat(new[] { "dry-runs.jsonl" }))
            if (File.Exists(Path.Combine(outDir, f))) File.Delete(Path.Combine(outDir, f));
        RunsLogOverride = Path.Combine(outDir, "dry-runs.jsonl");
        var standIn = new FfStandIn();
        int days = 0;
        var day = DateTime.Today.AddDays(1);
        string firstDayStop = null;
        while (FfComplete(FfRead(Path.Combine(outDir, "turns.jsonl"))).Count < FfTriples && days < 8)
        {
            days++;
            KeyTask = "measure-" + day.ToString("yyyy-MM-dd");
            double limit = Math.Max(0, CapOf(KeyTask) - KeyTaskSpent());
            _keyRun = new KeyRun { Client = new BudgetedClient(standIn, limit), What = "DRY RUN of the faster first sentence's bench, day " + days };
            using (var counted = new Counted(_keyRun))
            using (var timed = new FfTimed(counted))
            {
                Console.WriteLine($"dry run, day {days} ({KeyTask}): held to US${limit:0.000}");
                var (turns, stopped) = await FfDay(timed, _keyRun.Client, null, outDir, "dry-" + days, int.Parse(Arg(args, "--triples", "0")));
                if (days == 1) firstDayStop = stopped;
                LogKeyRun(turns, stopped);
            }
            day = day.AddDays(1);
        }
        // Stand-in readings, so every line of the scorer runs: every pair equal, nothing invented.
        FfScore(outDir, true);
        WriteJsonl(Path.Combine(outDir, "reading-pairs.jsonl"), ReadJsonl<JsonElement>(Path.Combine(outDir, "blind-pairs.jsonl"))
            .Select(p => new { id = p.GetProperty("id").GetString(), better = "equal", padded = new string[0], repeats = new string[0], contradicts = new string[0] }));
        WriteJsonl(Path.Combine(outDir, "reading-lines.jsonl"), ReadJsonl<JsonElement>(Path.Combine(outDir, "blind-lines.jsonl"))
            .Select(p => new { id = p.GetProperty("id").GetString(), invented = new string[0] }));
        FfScore(outDir, true);
        // What the dry run must show.
        var all = FfRead(Path.Combine(outDir, "turns.jsonl"));
        var whole = FfComplete(all);
        var log = File.ReadAllLines(RunsLogOverride).Where(l => l.Trim().Length > 0).Select(l => JsonDocument.Parse(l).RootElement).ToList();
        var faults = new List<string>();
        if (whole.Count != FfTriples) faults.Add($"{whole.Count} of {FfTriples} triples complete");
        if (days < 2 || log.Count != days) faults.Add($"the run was not split over days by the cap ({days} days, {log.Count} log lines)");
        if (log.Any(r => r.GetProperty("usd").GetDouble() > 1.0)) faults.Add("a day spent more than its dollar");
        var turnsOf = whole.Values.SelectMany(t => t.Values).ToList();
        bool Draft(FfCall c) => c.kind == "draft";
        if (!turnsOf.Where(t => t.arm == "A").All(t => t.calls.Where(Draft).All(c => c.thinking == null))) faults.Add("an A draft sent a thinking setting");
        if (!turnsOf.Where(t => t.arm != "A").All(t => t.calls.Where(c => Draft(c) || c.kind == "rest" || c.kind == "fast").All(c => c.thinking == "disabled"))) faults.Add("an A0 or B draft thought");
        int bFast = turnsOf.Count(t => t.arm == "B" && t.firstFast), bTurns = turnsOf.Count(t => t.arm == "B");
        if (bFast < bTurns / 2) faults.Add($"B's first sentence by Haiku in only {bFast} of {bTurns} turns");
        if (turnsOf.Any(t => t.arm != "B" && (t.firstFast || t.calls.Any(c => c.kind == "fast" || c.kind == "rest")))) faults.Add("the split ran outside arm B");
        if (!turnsOf.Where(t => t.arm == "B").SelectMany(t => t.calls).Any(c => c.kind == "rest")) faults.Add("no rest was asked for under the stricter note");
        if (!standIn.SawStrictNote) faults.Add("the stricter note never reached the rest's model");
        if (turnsOf.Any(t => t.scoreFound == null)) faults.Add("a turn without its scoring check");
        if (!turnsOf.Any(t => t.firstRefused)) faults.Add("no first sentence was refused, so the refusal path never ran");
        foreach (var f in FfOwnFiles)
            if (!File.Exists(Path.Combine(outDir, f))) faults.Add("no " + f);
        if (File.Exists(Path.Combine(RepoRoot(), "production", "playtest", "talk-runs.jsonl"))
            && File.ReadAllText(Path.Combine(RepoRoot(), "production", "playtest", "talk-runs.jsonl")).Contains("DRY RUN")) faults.Add("the dry run wrote to the repository's log");
        if (standIn.Calls == 0) faults.Add("the stand-in was never asked");
        Console.WriteLine($"dry run: {whole.Count} triples over {days} days (day 1 stopped: {firstDayStop ?? "never"}), {standIn.Calls} stand-in calls, no network, no key read; " +
                          $"B's first sentence by Haiku in {bFast} of {bTurns} turns");
        if (faults.Count > 0) { Console.WriteLine("dry run: FAILED: " + string.Join("; ", faults)); return 1; }
        Console.WriteLine("dry run: ok");
        return 0;
    }

    /// A MODEL THAT ANSWERS BY THE KIND OF REQUEST, for the dry run: the check's list (a sentence with a van in it names
    /// one the facts lack), its second look (never supported), the faster model's first sentence, the rest, a whole
    /// reply (thinking a little first when not told otherwise), and anything else an empty answer. Its tokens are what
    /// it was sent and wrote, at four characters a token, so the day's dollar runs out as the real one would.
    sealed class FfStandIn : IStartingLlmClient
    {
        int _calls;
        public int Calls => _calls;
        public volatile bool SawStrictNote;

        static string Kind(LlmRequest r) =>
            r.System != null && r.System.StartsWith("You read one line", StringComparison.Ordinal) ? "list"
            : r.System != null && r.System.StartsWith("You check details", StringComparison.Ordinal) ? "look"
            : r.System != null && r.System.Contains("YOUR REPLY HAS ALREADY BEGUN") ? "rest"
            : r.MaxTokens == ConversationEngine.FirstMaxTokens && r.Model == FfFastModel ? "fast"
            : r.MaxTokens == 300 ? "draft" : "other";

        static string LastUser(LlmRequest r) => r.Messages.Count == 0 ? "" : r.Messages[r.Messages.Count - 1].Content ?? "";

        string Answer(LlmRequest r, string kind)
        {
            string user = LastUser(r);
            int h = Math.Abs(user.GetHashCode() % 7);
            switch (kind)
            {
                case "list":
                    return user.Contains(" van") ? "{\"specifics\": [{\"detail\": \"a white van\", \"kind\": \"vehicle\", \"source\": \"none\"}]}" : "{\"specifics\": []}";
                case "look":
                    return "{\"verdicts\": [{\"n\": 1, \"supported\": false}]}";
                case "fast":
                    return h == 0 ? "A white van went by early on. {H1} Not much else." : "I keep myself to myself, mostly. {C1} Ask at the office.";
                case "rest":
                    if (r.System.Contains("Most replies end there")) SawStrictNote = true;
                    return h % 2 == 0 ? "" : "Ask at the office if you want more. {C2}";
                case "draft":
                    // the second draft is told what the first claimed; it claims nothing
                    if (r.System.Contains("van")) return "Couldn't tell you, love. {C1}";
                    return h == 1 ? "A white van went by early on. {H1} Not much else to tell." : "I keep myself to myself, mostly. {C1} Ask at the office if you want more. {C2}";
                default:
                    return "{}";
            }
        }

        LlmResponse Response(LlmRequest r, string text, int extraOut) => new LlmResponse
        {
            Text = text, StopReason = "end_turn", Model = r.Model,
            InputTokens = ((r.System ?? "").Length + r.Messages.Sum(m => (m.Content ?? "").Length)) / 4,
            OutputTokens = text.Length / 4 + 1 + extraOut,
        };

        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default) => StreamAsync(request, null, null, ct);
        public Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default) => StreamAsync(request, onText, null, ct);

        public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, Action onStart, CancellationToken ct = default)
        {
            Interlocked.Increment(ref _calls);
            string kind = Kind(request);
            string text = Answer(request, kind);
            bool sonnet = request.Model == Models.Core;
            await Task.Delay(sonnet ? 40 : kind == "fast" ? 12 : 20, ct);
            onStart?.Invoke();
            // Sonnet 5 thinks when not told otherwise: a pause before its first words, and tokens for it.
            bool thinks = sonnet && request.Thinking == null;
            if (thinks) await Task.Delay(25, ct);
            int cut = text.IndexOf(". ", StringComparison.Ordinal);
            if (cut > 0 && (kind == "draft" || kind == "fast" || kind == "rest"))
            {
                onText?.Invoke(text.Substring(0, cut + 3));
                try { await Task.Delay(20, ct); }
                catch (OperationCanceledException)
                {
                    throw new LlmStreamStoppedException(Response(request, text.Substring(0, cut + 3), thinks ? 60 : 0), ct);
                }
            }
            onText?.Invoke(text);
            return Response(request, text, thinks ? 60 : 0);
        }
    }

    /// EACH CALL'S MOMENTS, for the bench: sent, begun (the model's first content, thinking included), first words, end,
    /// from the turn's start; passed through to the client underneath unchanged.
    sealed class FfTimed : IStartingLlmClient, IDisposable
    {
        readonly IStartingLlmClient _inner;
        readonly object _gate = new object();
        Stopwatch _clock = Stopwatch.StartNew();
        List<FfCall> _calls = new List<FfCall>();
        public FfTimed(IStartingLlmClient inner) => _inner = inner;

        public void Begin() { lock (_gate) { _calls = new List<FfCall>(); _clock = Stopwatch.StartNew(); } }
        public List<FfCall> End() { lock (_gate) { var c = _calls; _calls = new List<FfCall>(); return c; } }
        long Now() { lock (_gate) return _clock.ElapsedMilliseconds; }

        static string Kind(LlmRequest r) =>
            r.System != null && (r.System.StartsWith("You read one line", StringComparison.Ordinal) || r.System.StartsWith("You check details", StringComparison.Ordinal)) ? "check"
            : r.System != null && r.System.Contains("YOUR REPLY HAS ALREADY BEGUN") ? "rest"
            : r.MaxTokens == ConversationEngine.FirstMaxTokens && r.Model == ConversationEngine.FirstModel ? "fast"
            : r.MaxTokens == 300 ? "draft" : "other";

        FfCall Open(LlmRequest r)
        {
            var c = new FfCall { kind = Kind(r), model = r.Model, thinking = r.Thinking };
            lock (_gate) { c.sentMs = _clock.ElapsedMilliseconds; _calls.Add(c); }
            return c;
        }

        void Close(FfCall c, LlmResponse r, string how)
        {
            lock (_gate) { c.endMs = _clock.ElapsedMilliseconds; c.ended = how; if (r != null) { c.inTok = r.InputTokens; c.outTok = r.OutputTokens; } }
        }

        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            var c = Open(request);
            try { var r = await _inner.CompleteAsync(request, ct).ConfigureAwait(false); Close(c, r, "end"); return r; }
            catch (Exception) { Close(c, null, "failed"); throw; }
        }

        public Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default) => StreamAsync(request, onText, null, ct);

        public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, Action onStart, CancellationToken ct = default)
        {
            var c = Open(request);
            try
            {
                var r = await _inner.StreamAsync(request,
                    text => { lock (_gate) if (c.firstTextMs < 0) c.firstTextMs = _clock.ElapsedMilliseconds; onText?.Invoke(text); },
                    () => { lock (_gate) if (c.begunMs < 0) c.begunMs = _clock.ElapsedMilliseconds; onStart?.Invoke(); }, ct).ConfigureAwait(false);
                Close(c, r, "end");
                return r;
            }
            catch (LlmStreamStoppedException e) { Close(c, e.SoFar, "stopped"); throw; }
            catch (Exception) { Close(c, null, "failed"); throw; }
        }

        /// The client underneath belongs to whoever made it, and is disposed there.
        public void Dispose() { }
    }
}
