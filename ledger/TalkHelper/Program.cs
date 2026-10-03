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
/// With --early (26 September, the voice's delay): first, as soon as the reply's
/// first sentence is written and has passed its own check,
///      {"id":1,"to":"sam","first":"...","ms":640}
/// and then the usual line, with "rest": what follows the first sentence, the
/// only part still to be spoken.
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
/// AND WHAT THEY HAVE HEARD OF HIS NIGHTS, 28 September (Jafar: someone who
/// knows even a little treats him slightly differently): the game sends the
/// street's own count (StreetVoice.RegardFor's Knowing and Story), and only
/// when RegardFor says they can tell it is him (KnowsItIsHim; otherwise
/// "nothing"), since somebody who has only heard of him does not know the man
/// in front of them is the one the story is about,
///   "knowing":{"level":"little"|"enough"|"nothing","story":"..."}
/// and while nothing ties him to a deed the character is given the manner that
/// story gives them instead of being at ease with him; the reply's "manner"
/// says which ("little" or "enough", as sent) or is null.
///
/// FAKE MODE, --fake (or LEDGER_TALK_FAKE=1), for the encounter's regression:
/// no key, no network, no cost. A stand-in model answers from the memories in
/// its prompt - it asks about the first one it was given, or passes the time
/// of day when it was given none - so a test can see knowledge arrive in the
/// answer without paying for a model.
/// The key is read from ANTHROPIC_API_KEY and never printed. With --relay
/// <address> the helper holds no key: it sends a copy's code (--copy, or
/// LEDGER_COPY) to our relay (ledger/Relay), which holds it.
static class Program
{
    static readonly string[] BrushOffs =
    {
        "Not now. Busy.",
        "Catch me later, eh?",
        "Can't stop. Another time.",
    };

    // THE REPLY AS WRITTEN: apostrophes and accents stay themselves rather
    // than escape codes, so a log or a transcript reads as the line was said.
    static readonly JsonSerializerOptions Plain = new JsonSerializerOptions { Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping };
    static readonly PlayerIdentity Tom = new PlayerIdentity();

    sealed class Helper
    {
        public readonly Dictionary<string, CharacterCard> Cards = new Dictionary<string, CharacterCard>();
        /// Whether each person trusts Tom, as the game last said (the acquaintance's
        /// "trusts"): only somebody the cast file names on trust reads it.
        readonly Dictionary<string, bool> _trusts = new Dictionary<string, bool>();
        // When Ron last asked him plainly whether to tell them no, per person
        // (town list 6bn): his plain yes as his next line in that conversation,
        // within three game hours, is the no; walking away or a fresh
        // conversation clears it.
        readonly Dictionary<string, GameTime> _askedNo = new Dictionary<string, GameTime>();
        // Which answer Sheila last asked him plainly to confirm, per person
        // (town list 6ca): his plain yes as his very next line, to her, is his
        // answer; any other line, a walk-off, a fresh talk or a load clears it.
        readonly Dictionary<string, WeekAnswer> _askedWeek = new Dictionary<string, WeekAnswer>();

        /// The named cast's routines (production/specs/hook-cast.json), so each
        /// person is told where they are this hour (town list 6u); null without.
        public CastDay Cast;
        /// The scene the last line was answered in (the selftest reads it).
        public string LastScene;
        readonly Dictionary<string, ConversationEngine> _engines = new Dictionary<string, ConversationEngine>();
        readonly ILlmClient _llm;
        readonly CostTracker _cost = new CostTracker();

        // WALKING OFF STOPS THE REPLY AT ONCE (town list 6ay, the fourth sweep):
        // lines were read one at a time, so "walkedAway" was read only after the
        // reply it was about had finished, paid for, and the next person waited
        // behind it. The reader now hands such a line here the moment it arrives
        // (WalkOffIfFor); the reply being written for that person stops.
        readonly System.Collections.Concurrent.ConcurrentDictionary<string, CancellationTokenSource> _walkCts =
            new System.Collections.Concurrent.ConcurrentDictionary<string, CancellationTokenSource>();
        readonly System.Collections.Concurrent.ConcurrentDictionary<string, string> _walkHeard =
            new System.Collections.Concurrent.ConcurrentDictionary<string, string>();
        readonly HashSet<string> _walkedHandled = new HashSet<string>();

        /// A line that arrived while a reply was being written: when it says he
        /// walked away from the person being answered, that reply stops now.
        public bool WalkOffIfFor(string line)
        {
            try
            {
                using var doc = JsonDocument.Parse(line);
                if (!doc.RootElement.TryGetProperty("walkedAway", out var wa) || wa.ValueKind != JsonValueKind.Object) return false;
                string from = wa.TryGetProperty("to", out var t) && t.ValueKind == JsonValueKind.String ? t.GetString() : null;
                string heard = wa.TryGetProperty("heard", out var h) && h.ValueKind == JsonValueKind.String ? h.GetString() : "";
                if (from == null || !_walkCts.TryGetValue(from, out var stop)) return false;
                _walkHeard[from] = heard ?? "";
                try { stop.Cancel(); } catch (ObjectDisposedException) { return false; }
                return true;
            }
            catch (JsonException) { return false; }
        }
        public CostTracker Cost => _cost;
        readonly TimeSpan _patience;

        public Helper(ILlmClient llm, TimeSpan patience) { _llm = llm; _patience = patience; }
        public bool Early;
        /// THE FIRST SENTENCE AHEAD OF ITS CHECK (--pending; U1, 30 September):
        /// with Early, each first sentence is also written the moment it is
        /// drafted as {"id","to","pending":...,"ms"}, before its check, so the
        /// game's voice can make it ready while it is checked. It is to be
        /// PLAYED only when the same turn's "first" arrives with the same words;
        /// a pending sentence with no matching "first" before the turn's reply
        /// is never played. Off unless asked for, until the game reads it.
        public bool Pending;
        /// Threats the words miss read by the checking model beside the reply
        /// (ThreatRead; Jafar, 30 September), and how long past the reply the
        /// turn waits for it.
        public bool ThreatByModel = true;
        public TimeSpan ThreatWait = TimeSpan.FromSeconds(2);
        /// THE REST'S OWN LIMIT (town list 6bx): once the first sentence has
        /// been heard, the rest of the reply has this long beyond the turn's
        /// patience before it is cut, so a turn whose first words came quickly
        /// is not thrown away at eight seconds as a brush-off. The player is
        /// already listening; what is cut is recorded "cut".
        public TimeSpan RestPatience = TimeSpan.FromSeconds(6);
        // A turn abandoned at the patience limit may still be unwinding; the
        // same character's next line waits for it (the independent check: a
        // late unwind disturbed the next turn's transcript).
        readonly Dictionary<ConversationEngine, Task> _unwinding = new Dictionary<ConversationEngine, Task>();
        // Where an early first sentence is written (the selftest listens here).
        public Action<string> Emit = line => { lock (Console.Out) { Console.Out.WriteLine(line); Console.Out.Flush(); } };
        // The claim check on a stand-in model too, for the selftest.
        public bool CheckAlways;

        public bool Online => _llm != null;

        /// Whether this person trusts Tom now: the game said so, or their own
        /// talk with him has earned it (town list 6bz). The game's "false" is
        /// only that it has not decided so: it never undoes trust earned (the
        /// independent check: a game keeping a plain false never got her trust).
        bool TrustsHim(string key, ConversationEngine engine)
        {
            lock (_trusts)
                return (_trusts.TryGetValue(key, out var said) && said) || (engine != null && engine.TrustEarned);
        }

        /// For somebody who names him only on trust, whether they trust him
        /// after this turn, and whether this turn earned it; null and false for
        /// anybody else. Earned only on a turn they answered in their own
        /// words, or with live talk off, when no turn ever is (the independent
        /// check: a brush-off turn earned it, and with talk off nothing could).
        (bool? trusts, bool earned) TrustAfter(string key, ConversationEngine engine, int day, bool canEarn)
        {
            if (Cast == null || !Cast.NamesHimOnlyOnTrust(key)) return (null, false);
            bool gameSaid;
            lock (_trusts) gameSaid = _trusts.TryGetValue(key, out var said) && said;
            // Trust the game already granted is never announced again (the
            // independent check: the book's cue could come twice).
            bool earned = canEarn && Trust.Earn(engine, day) && !gameSaid;
            return (TrustsHim(key, engine), earned);
        }

        // Locked: a suggestion reads it off the one-at-a-time queue.
        public ConversationEngine EngineFor(string to) { lock (_engines) return _engines.TryGetValue(to, out var e) ? e : null; }

        /// Whether a line is a request for Tom's suggested lines ({"kind":"suggest"}).
        public static bool IsSuggest(string line)
        {
            if (line == null || line.IndexOf("\"suggest\"", StringComparison.Ordinal) < 0) return false;
            try
            {
                using var d = JsonDocument.Parse(line);
                return d.RootElement.ValueKind == JsonValueKind.Object && d.RootElement.TryGetProperty("kind", out var k)
                    && k.ValueKind == JsonValueKind.String && k.GetString() == "suggest";
            }
            catch (JsonException) { return false; }
        }

        /// TOM'S WRITTEN SUGGESTED LINES (production/specs/suggested-lines.json),
        /// for the suggestions the model does not write; empty without the file.
        public Suggest.Written Written = new Suggest.Written();
        /// True with the stand-in (--fake): suggestions are then all written ones.
        public bool Fake;
        // What has been suggested to Tom in each conversation, by person and the
        // engine's TalkNumber, so nothing is offered twice in one conversation.
        readonly Dictionary<string, (int talk, List<string> lines)> _suggested = new Dictionary<string, (int talk, List<string> lines)>();

        /// THE SUGGESTED LINES (Jafar, 1 October: "Mixed"; production/design/ui/
        /// STYLE-GUIDE.md): three lines Tom could say next to `key`, from a call
        /// of their own given only his Ledger (`tomKnows`), how he knows them
        /// (`with`) and the talk so far; the written lines without a model.
        async Task<string> SuggestAsync(int id, string to, string key, List<string> tomKnows, string with, List<string> shownByGame = null)
        {
            var engine = EngineFor(key);
            IReadOnlyList<LlmMessage> heard = engine != null ? engine.TalkSoFar : new List<LlmMessage>();
            int talk = engine?.TalkNumber ?? 0;
            List<string> shown;
            lock (_suggested)
            {
                if (!_suggested.TryGetValue(key, out var s) || s.talk != talk) _suggested[key] = s = (talk, new List<string>());
                if (shownByGame != null) foreach (var l in shownByGame) if (!string.IsNullOrWhiteSpace(l) && !s.lines.Contains(l)) s.lines.Add(l);
                shown = new List<string>(s.lines);
            }
            var r = await Suggest.WriteAsync(Fake ? null : _llm, Written, tomKnows, new List<LlmMessage>(heard), with, shown, id, _cost, TimeSpan.FromSeconds(6));
            lock (_suggested)
                if (_suggested.TryGetValue(key, out var s) && s.talk == talk)
                    foreach (var l in r.Lines) if (l != null) s.lines.Add(l);
            // In the jobs' order, a job with no line left out; `jobs` names each.
            var jobNames = new[] { "ask", "personal", "leave" };
            var lines = new List<string>(); var jobs = new List<string>(); var made = new List<bool>();
            for (int j = 0; j < Suggest.Jobs; j++)
                if (r.Lines[j] != null) { lines.Add(r.Lines[j]); jobs.Add(jobNames[j]); made.Add(r.Generated[j]); }
            return JsonSerializer.Serialize(new { id, to, suggest = lines, jobs, generated = made, model = r.Model }, Plain);
        }

        ConversationEngine NewEngine(CharacterCard card)
        {
            var engine = new ConversationEngine(_llm, card, new MemoryStore(card.Id), new KnowledgeBase(),
                new SuspicionTracker(), _cost);
            // THE CLAIM CHECK ON THE REAL MODEL (ClaimCheck.cs, 24 September):
            // every reply is read for claims the character's knowledge does
            // not support before it is said. Not on the stand-in models,
            // which answer only from memory already.
            if (ChecksReplies(_llm, CheckAlways)) engine.Checker = _llm;
            return engine;
        }

        /// WHETHER EVERY REPLY THIS CLIENT WRITES IS CHECKED before it is said: the
        /// real model is; the stand-ins, which answer only from memory, are not.
        /// LOOKED FOR THROUGH THE KEY'S CAP (P3, 3 October): BudgetedClient wraps the real model, and
        /// asking only "is this the Anthropic client" turned the check off for every capped run, the
        /// only in-game measurement of real talk (30 September) among them.
        internal static bool ChecksReplies(ILlmClient llm, bool checkAlways)
        {
            while (llm is BudgetedClient capped) llm = capped.Inner;
            return checkAlways || llm is AnthropicClient;
        }

        /// TALK KEPT WITH THE GAME'S SAVE (town list 6r, the checklist sweep of 28
        /// September): what Tom said to each person lived only in here, so a
        /// reload forgot it and a new game carried it over.
        ///   {"talk":"save","path":P}  every conversation, written to P
        ///   {"talk":"load","path":P}  every conversation replaced by P's
        ///   {"talk":"reset"}          every conversation forgotten (a new game)
        /// P must end ".talk.json", beside the game's own save, so a slip in the
        /// game cannot make this write over anything else.
        public async Task<string> Talk(string op, string path, string stamp = null)
        {
            op = (op ?? "").Trim().ToLowerInvariant();
            // A LOAD OR A RESET FORGETS EVERYBODY FIRST, whatever else fails: the
            // timeline the player left is gone either way (the independent check:
            // a load with a bad path kept the old talk).
            if (op == "reset" || op == "load")
            {
                lock (_engines) _engines.Clear();
                _unwinding.Clear();
                // Trust is the game's to say again for the timeline it loads.
                lock (_trusts) _trusts.Clear();
                lock (_askedNo) { _askedNo.Clear(); _askedWeek.Clear(); }
                if (op == "reset") return JsonSerializer.Serialize(new { talk = "reset" }, Plain);
            }
            if (op != "save" && op != "load") return JsonSerializer.Serialize(new { talk = op, error = "unknown" }, Plain);
            if (string.IsNullOrWhiteSpace(path) || !path.EndsWith(".talk.json", StringComparison.OrdinalIgnoreCase))
                return JsonSerializer.Serialize(new { talk = op, error = "path-must-end-.talk.json" }, Plain);
            if (op == "save")
            {
                // A turn given up at the patience limit may still be finishing:
                // wait for it (as the next turn does), or the save keeps a line
                // nobody heard, read while it is being written.
                foreach (var t in new List<Task>(_unwinding.Values)) await Task.WhenAny(t, Task.Delay(10000));
                _unwinding.Clear();
                string tmp = path + ".tmp";
                try
                {
                    var people = new Dictionary<string, object>();
                    lock (_engines) foreach (var kv in _engines) people[kv.Key] = kv.Value.CaptureTalk();
                    var root = new Dictionary<string, object> { { "version", 1 }, { "people", people } };
                    if (!string.IsNullOrEmpty(stamp)) root["stamp"] = stamp;
                    File.WriteAllText(tmp, MiniJson.Serialize(root));
                    File.Move(tmp, path, overwrite: true);
                    return JsonSerializer.Serialize(new { talk = "saved", people = people.Count }, Plain);
                }
                catch (Exception)
                {
                    // A FAILED SAVE LEAVES NO TALK AT ALL in the slot, never an
                    // older timeline's: a load then finds none, and nobody knows
                    // what they were never told (the independent check).
                    try { if (File.Exists(tmp)) File.Delete(tmp); } catch (Exception) { }
                    try { if (File.Exists(path)) File.Delete(path); } catch (Exception) { }
                    return JsonSerializer.Serialize(new { talk = "save", error = "unwritable" }, Plain);
                }
            }
            if (!File.Exists(path)) return JsonSerializer.Serialize(new { talk = "loaded", people = 0, missing = true }, Plain);
            Dictionary<string, object> saved;
            try { saved = MiniJson.AsObject(MiniJson.Deserialize(File.ReadAllText(path))); }
            catch (Exception) { saved = null; }
            var list = MiniJson.GetObject(saved, "people");
            if (list == null) return JsonSerializer.Serialize(new { talk = "loaded", people = 0, error = "unreadable" }, Plain);
            // THE STAMP (the independent check): the game names each save with its
            // own id and sends it with "save" and with "load". Talk stamped for
            // another save, left behind by a save that could not replace it, is
            // never loaded: nobody knows what they were told in another game.
            string onFile = MiniJson.GetString(saved, "stamp");
            if (!string.IsNullOrEmpty(stamp) && onFile != stamp)
                return JsonSerializer.Serialize(new { talk = "loaded", people = 0, stale = true }, Plain);
            int skipped = 0;
            foreach (var kv in list)
            {
                var state = MiniJson.AsObject(kv.Value);
                string cardId = MiniJson.GetString(state, "card");
                // By the card's own id, not its file name (sam.md copied as darren.md).
                CharacterCard card = null;
                if (cardId != null) foreach (var c in Cards.Values) if (c.Id == cardId) { card = c; break; }
                if (state == null || card == null) { skipped++; continue; }
                var engine = NewEngine(card);
                engine.RestoreTalk(state);
                lock (_engines) _engines[kv.Key] = engine;
            }
            return JsonSerializer.Serialize(new { talk = "loaded", people = _engines.Count, skipped }, Plain);
        }

        /// A TURN AS THE PLAYER HAD IT, kept for a report (town list 6c: Steam,
        /// Microsoft and PEGI all require a way to report what the AI said):
        /// the last hundred, what was said to whom and what came back.
        public sealed class Turn
        {
            public int Id { get; set; }
            public string To { get; set; }
            public int Day { get; set; }
            public int Hour { get; set; }
            public int Minute { get; set; }
            public string Say { get; set; }
            public string Reply { get; set; }
            public bool Generated { get; set; }
            public string Model { get; set; }
            public List<string> Invented { get; set; }
            public bool Unchecked { get; set; }
            public long Ms { get; set; }
        }
        readonly List<Turn> _turns = new List<Turn>();
        /// Where a report is kept when it cannot be sent.
        public string ReportsDir = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "LEDGER", "reports");
        /// Sends a report to our relay; null when the helper talks to the provider directly.
        public Func<string, Task<bool>> SendReport;

        void Keep(Turn t)
        {
            lock (_turns)
            {
                _turns.Add(t);
                if (_turns.Count > 100) _turns.RemoveAt(0);
            }
        }

        /// THE PLAYER REPORTS A LINE: {"report": <the turn's id>, "why": "..."}.
        /// Sent to our relay when there is one, else (or when sending fails)
        /// kept on this PC; either way the answer says where it went.
        async Task<string> ReportAsync(int id, string why)
        {
            Turn t = null;
            lock (_turns) for (int i = _turns.Count - 1; i >= 0 && t == null; i--) if (_turns[i].Id == id) t = _turns[i];
            if (t == null) return JsonSerializer.Serialize(new { reported = id, found = false }, Plain);
            why = why ?? "";
            if (why.Length > 500) why = why.Substring(0, 500);
            var record = JsonSerializer.Serialize(new { reportedAt = DateTime.UtcNow.ToString("O"), why, turn = t }, Plain);
            string saved = "local";
            if (SendReport != null)
            {
                try { if (await SendReport(record)) saved = "relay"; } catch (Exception) { }
            }
            if (saved == "local")
            {
                try
                {
                    Directory.CreateDirectory(ReportsDir);
                    File.AppendAllText(Path.Combine(ReportsDir, "reports.jsonl"), record + "\n");
                }
                catch (Exception) { saved = "lost"; }
            }
            return JsonSerializer.Serialize(new { reported = id, found = true, saved, thanks = AiNotice.ReportThanks(saved) }, Plain);
        }

        public async Task<string> Answer(string line)
        {
            int id = 0;
            string to = "", say = "", scene = "";
            int hour = 12, day = 1, minute = 0;
            var memories = new List<MemoryEvent>();
            var storyOfMemory = new Dictionary<MemoryEvent, string>();
            var knows = new List<Fact>();
            double? suspicion = null;
            string suspicionWhy = null;
            string who = null;
            bool noReply = false;
            (double value, SuspicionLevel level, string why)? derived = null;
            bool knowingSent = false;
            var knowing = Knowing.Nothing;
            string knowingStory = null;
            int? report = null;
            string reportWhy = null;
            string talkOp = null, talkPath = null, talkStamp = null;
            string walkedFrom = null, walkedHeard = null;
            string deedTopic = null, sawHimAt = null, heardHimAt = null; int deedDay = -1, deedHour = -1; bool deedGrave = false;
            bool askTonight = false;
            bool weekAsk = false, weekStands = false, weekRealBook = false, weekDayOff = false, weekEnded = false;
            bool sawHimNear = false;
            var heardHeSaid = new List<string>();
            bool acquaintanceSent = false, metHim = false, heardOfHim = false, fresh = false;
            bool? trustsSent = null;
            string callsHim = null;
            bool knowsNameSent = false, gaveNameOut = false, callsSentByGame = false;
            List<string> present = null;
            string evidenceTopic = null;
            bool evidenceSent = false; string momentSaid = null;
            bool suggestAsked = false; var tomKnows = new List<string>(); string suggestWith = null; var suggestShown = new List<string>();
            try
            {
                using var doc = JsonDocument.Parse(line);
                var r = doc.RootElement;
                if (r.TryGetProperty("report", out var rp) && rp.ValueKind == JsonValueKind.Number)
                {
                    report = rp.GetInt32();
                    if (r.TryGetProperty("why", out var rw) && rw.ValueKind == JsonValueKind.String) reportWhy = rw.GetString();
                }
                // THE DEED THEY SUSPECT HIM OF, and when (town list 6ac): what an answer
                // about where he was is about.
                if (r.TryGetProperty("deed", out var dd) && dd.ValueKind == JsonValueKind.Object
                    && dd.TryGetProperty("topic", out var dt) && dt.ValueKind == JsonValueKind.String)
                {
                    deedTopic = dt.GetString();
                    deedDay = dd.TryGetProperty("day", out var ddy) && ddy.ValueKind == JsonValueKind.Number ? ddy.GetInt32() : -1;
                    deedHour = dd.TryGetProperty("hour", out var dh) && dh.ValueKind == JsonValueKind.Number ? dh.GetInt32() : -1;
                    // Where this person saw him at about the deed's time, if they did.
                    sawHimAt = dd.TryGetProperty("sawHimAt", out var sa) && sa.ValueKind == JsonValueKind.String ? sa.GetString() : null;
                    // A grave deed (a killing): nobody keeps it quiet for the asking (town list 6al).
                    deedGrave = dd.TryGetProperty("grave", out var gv) && gv.ValueKind == JsonValueKind.True;
                    // Where they have heard he was, and where they have heard he says he was (town list 6am).
                    heardHimAt = dd.TryGetProperty("heardHimAt", out var hh) && hh.ValueKind == JsonValueKind.String ? hh.GetString() : null;
                    // One area id, or every area of the claim ("the fish market" is two).
                    if (dd.TryGetProperty("heardHeSaid", out var hs))
                    {
                        if (hs.ValueKind == JsonValueKind.String) heardHeSaid.Add(hs.GetString());
                        else if (hs.ValueKind == JsonValueKind.Array)
                            foreach (var he in hs.EnumerateArray()) if (he.ValueKind == JsonValueKind.String) heardHeSaid.Add(he.GetString());
                    }
                }
                // HE WALKED OFF MID-REPLY (town list 6v): who from, and what he heard.
                if (r.TryGetProperty("walkedAway", out var wa) && wa.ValueKind == JsonValueKind.Object)
                {
                    walkedFrom = wa.TryGetProperty("to", out var wt) && wt.ValueKind == JsonValueKind.String ? wt.GetString() : "";
                    walkedHeard = wa.TryGetProperty("heard", out var wh) && wh.ValueKind == JsonValueKind.String ? wh.GetString() : "";
                }
                // TOM'S SUGGESTED LINES (Jafar, 1 October): {"kind":"suggest"}, with his
                // Ledger ("tomKnows") and how he knows them ("with"), never theirs.
                if (r.TryGetProperty("kind", out var kd) && kd.ValueKind == JsonValueKind.String && kd.GetString() == "suggest")
                {
                    suggestAsked = true;
                    if (r.TryGetProperty("tomKnows", out var tkn) && tkn.ValueKind == JsonValueKind.Array)
                        foreach (var k in tkn.EnumerateArray()) if (k.ValueKind == JsonValueKind.String) tomKnows.Add(k.GetString());
                    if (r.TryGetProperty("with", out var wi) && wi.ValueKind == JsonValueKind.String) suggestWith = wi.GetString();
                    // Lines the game showed itself (the file's, before the answer came), so
                    // never-twice holds for them too.
                    if (r.TryGetProperty("shown", out var sh) && sh.ValueKind == JsonValueKind.Array)
                        foreach (var k in sh.EnumerateArray()) if (k.ValueKind == JsonValueKind.String) suggestShown.Add(k.GetString());
                }
                // What the game says the moment is (D48): "smalltalk" or "conversation".
                if (r.TryGetProperty("moment", out var mo) && mo.ValueKind == JsonValueKind.String) momentSaid = mo.GetString();
                if (r.TryGetProperty("talk", out var tk) && tk.ValueKind == JsonValueKind.String)
                {
                    talkOp = tk.GetString();
                    if (r.TryGetProperty("path", out var tp) && tp.ValueKind == JsonValueKind.String) talkPath = tp.GetString();
                    if (r.TryGetProperty("stamp", out var ts) && ts.ValueKind == JsonValueKind.String) talkStamp = ts.GetString();
                }
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
                        var mem = new MemoryEvent(
                            new GameTime(m.TryGetProperty("day", out var md) ? md.GetInt32() : day,
                                         m.TryGetProperty("hour", out var mh) ? mh.GetInt32() : hour,
                                         m.TryGetProperty("minute", out var mm) ? mm.GetInt32() : 0),
                            m.TryGetProperty("kind", out var mk) ? mk.GetString() ?? "observation" : "observation",
                            m.TryGetProperty("importance", out var mi) ? mi.GetDouble() : 0.5,
                            text);
                        memories.Add(mem);
                        // Which story it belongs to (town list 6ah), when the game says.
                        if (m.TryGetProperty("story", out var ms) && ms.ValueKind == JsonValueKind.String) storyOfMemory[mem] = ms.GetString();
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
                // A NEW CONVERSATION (town list 6ae): the game says so when he walks up again.
                if (r.TryGetProperty("fresh", out v) && v.ValueKind == JsonValueKind.True) fresh = true;
                // THE OUTFIT'S ASK, HAD AND NOT YET ANSWERED TONIGHT (town list 6bn):
                // the game says so for the person who brought it (Ron).
                if (r.TryGetProperty("ask", out var ak) && ak.ValueKind == JsonValueKind.Object
                    && ak.TryGetProperty("tonight", out var akt) && akt.ValueKind == JsonValueKind.True) askTonight = true;
                // THE WEEK'S END (town list 6ca): the game says when Sheila puts her
                // question (WeeksEnd.Ask just returned true) and while it stands.
                if (r.TryGetProperty("week", out var wk) && wk.ValueKind == JsonValueKind.Object)
                {
                    weekAsk = wk.TryGetProperty("ask", out var wkAsk) && wkAsk.ValueKind == JsonValueKind.True;
                    weekStands = wk.TryGetProperty("stands", out var wkStands) && wkStands.ValueKind == JsonValueKind.True;
                    weekRealBook = wk.TryGetProperty("realBook", out var wkBook) && wkBook.ValueKind == JsonValueKind.True;
                    weekDayOff = wk.TryGetProperty("dayOff", out var wkOff) && wkOff.ValueKind == JsonValueKind.True;
                    // Mickey's arrangement already ended (town list 6cc): she never offers it.
                    weekEnded = wk.TryGetProperty("ended", out var wkEnd) && wkEnd.ValueKind == JsonValueKind.True;
                }
                // WHO IS REALLY WITH THEM (town list 6ad), as cast ids, when the game knows.
                if (r.TryGetProperty("present", out v) && v.ValueKind == JsonValueKind.Array)
                {
                    present = new List<string>();
                    foreach (var pe in v.EnumerateArray()) if (pe.ValueKind == JsonValueKind.String) present.Add(pe.GetString());
                }
                if (r.TryGetProperty("evidence", out v) && v.ValueKind == JsonValueKind.Object)
                {
                    evidenceSent = true;
                    var acc = new DeedAccount();
                    var near = new Nearness();
                    double fam = 0.0;
                    if (v.TryGetProperty("account", out var a) && a.ValueKind == JsonValueKind.Object)
                    {
                        acc.Held = Bool(a, "held"); acc.SawItMyself = Bool(a, "seen"); acc.NamesHim = Bool(a, "names");
                        acc.Rung = a.TryGetProperty("rung", out var rg) && rg.ValueKind == JsonValueKind.Number ? rg.GetInt32() : -1;
                        acc.Confidence = a.TryGetProperty("confidence", out var c) && c.ValueKind == JsonValueKind.Number ? c.GetDouble() : 0.0;
                        acc.Summary = a.TryGetProperty("summary", out var sm) ? sm.GetString() : null;
                        // How surely the naming reached them; a game that does not send it yet gets the account's own.
                        acc.NamingConfidence = a.TryGetProperty("namingConfidence", out var nc) && nc.ValueKind == JsonValueKind.Number ? nc.GetDouble() : acc.Confidence;
                        evidenceTopic = a.TryGetProperty("topic", out var atp) && atp.ValueKind == JsonValueKind.String ? atp.GetString() : null;
                    }
                    if (v.TryGetProperty("near", out var n) && n.ValueKind == JsonValueKind.Object)
                    {
                        near.SawHimMyself = Bool(n, "sawHim"); near.HeardHeWasNear = Bool(n, "heard");
                        sawHimNear = near.SawHimMyself || near.HeardHeWasNear;
                        near.OthersNear = n.TryGetProperty("others", out var o) && o.ValueKind == JsonValueKind.Number ? o.GetInt32() : 0;
                        near.Summary = n.TryGetProperty("summary", out var ns) ? ns.GetString() : null;
                    }
                    if (v.TryGetProperty("familiarity", out var fv) && fv.ValueKind == JsonValueKind.Number) fam = fv.GetDouble();
                    // THE EVIDENCE IS ABOUT THE LINE'S DEED (the independent review of 1
                    // October, N1): an account of another deed is not used, so a witness
                    // is never told she holds nothing of what she saw; said on stderr.
                    if (evidenceTopic != null && deedTopic != null && evidenceTopic != deedTopic)
                        Console.Error.WriteLine("talk: evidence for " + evidenceTopic + " sent with a line about " + deedTopic + "; not used");
                    else derived = Suspecting.Derive(acc, near, fam);
                }
                // HOW THIS PERSON KNOWS TOM (town list 6s), as the game knows it:
                // whether they have met him, heard of him, and what they call him.
                if (r.TryGetProperty("acquaintance", out var aq) && aq.ValueKind == JsonValueKind.Object)
                {
                    acquaintanceSent = true;
                    metHim = Bool(aq, "met");
                    heardOfHim = Bool(aq, "heardOf");
                    callsHim = aq.TryGetProperty("calls", out var ac) && ac.ValueKind == JsonValueKind.String && ac.GetString().Trim().Length > 0 ? ac.GetString() : null;
                    // They hold his name as the street's fact (town list 6ch).
                    knowsNameSent = aq.TryGetProperty("knowsName", out var akn) && akn.ValueKind == JsonValueKind.True;
                    if (aq.TryGetProperty("trusts", out var tr) && (tr.ValueKind == JsonValueKind.True || tr.ValueKind == JsonValueKind.False))
                        trustsSent = tr.ValueKind == JsonValueKind.True;
                }
                if (r.TryGetProperty("knowing", out v) && v.ValueKind == JsonValueKind.Object)
                {
                    string lv = v.TryGetProperty("level", out var kl) && kl.ValueKind == JsonValueKind.String ? kl.GetString() : "";
                    knowing = lv == "little" ? Knowing.ALittle : lv == "enough" ? Knowing.Enough : Knowing.Nothing;
                    knowingStory = v.TryGetProperty("story", out var kst) && kst.ValueKind == JsonValueKind.String ? kst.GetString() : null;
                    knowingSent = true;
                }
            }
            catch (Exception)
            {
                return JsonSerializer.Serialize(new { error = "bad-line" }, Plain);
            }
            // A line to anybody but Ron clears his question, even one that goes no
            // further than here (town list 6bn, the independent check).
            if (!string.IsNullOrEmpty(say) && to != Arrangement.Doorman) lock (_askedNo) _askedNo.Clear();
            if (!string.IsNullOrEmpty(say) && to != WeeksEnd.Sheila) lock (_askedNo) _askedWeek.Clear();
            if (suggestAsked)
            {
                if (!Cards.ContainsKey(to)) return JsonSerializer.Serialize(new { id, to, error = "no-card" }, Plain);
                return await SuggestAsync(id, to, string.IsNullOrEmpty(who) ? to : who, tomKnows, suggestWith, suggestShown);
            }
            if (talkOp != null) return await Talk(talkOp, talkPath, talkStamp);
            if (walkedFrom != null)
            {
                bool already;
                lock (_walkedHandled) already = _walkedHandled.Remove(walkedFrom);
                if (already) return JsonSerializer.Serialize(new { walkedAway = walkedFrom, noted = true }, Plain);
                var left = EngineFor(walkedFrom);
                if (left != null) left.WalkedAway(walkedHeard, new GameTime(day, hour, minute));
                lock (_askedNo) { _askedNo.Remove(walkedFrom); _askedWeek.Remove(walkedFrom); }
                return JsonSerializer.Serialize(new { walkedAway = walkedFrom, noted = left != null }, Plain);
            }
            if (report.HasValue) return await ReportAsync(report.Value, reportWhy);
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
            // WHERE THIS PERSON IS, from their routine at this hour, beside the
            // scene the game sends (the same for everybody until now).
            var where = Cast?.WhereWords(key, day, hour);
            if (where != null) scene = (string.IsNullOrWhiteSpace(scene) ? "" : scene.Trim() + " ") + "Where you are: " + where + ".";
            LastScene = scene;

            var sw = Stopwatch.StartNew();
            // Their own words when too busy to talk (town list 6ap), else the shared ones.
            var ownBrush = card.Own("brush-off");
            string brush = ownBrush.Count > 0 ? ownBrush[Math.Abs(id) % ownBrush.Count] : BrushOffs[Math.Abs(id) % BrushOffs.Length];
            var now = new GameTime(day, hour, minute);

            if (!_engines.TryGetValue(key, out var engine))
            {
                engine = NewEngine(card);
                lock (_engines) _engines[key] = engine;
            }
            // A day he talked with them, live talk or none (town list 6bz).
            if (!string.IsNullOrWhiteSpace(say)) engine.TalkDays.Add(day);
            // A card lent to somebody else: their name is not the card's
            // (town list 6be, the independent check).
            engine.SpeakerName = key != to ? "" : null;
            // WHO THEY KNOW, AND WHERE (town list 6ad), from the cast file this hour.
            if (Cast != null) engine.People = Cast.PeopleFor(key, day, hour, present);
            if (Cast != null) engine.StreetHours = Cast.HoursFor(day, hour, minute);
            // THE SIMULATION'S STATE, loaded before the line is answered.
            foreach (var m in memories)
            {
                bool held = false;
                foreach (var e in engine.Memory.Events)
                    if (e.Time.Equals(m.Time) && e.Text == m.Text) { held = true; break; }
                if (!held) engine.Memory.Append(m);
                if (storyOfMemory.TryGetValue(m, out var st)) engine.TagStory(m, st);
            }
            foreach (var f in knows) engine.Knowledge.Learn(f);
            if (fresh) { engine.StartFresh(); engine.GameMarksFresh = true; lock (_askedNo) { _askedNo.Remove(key); _askedWeek.Remove(key); } }
            // Kept until the game sends it again; until the game has ever sent it,
            // read off this conversation's own earlier talk with him.
            // Met is the game's word or their own earlier talk: the game cannot
            // make them forget a conversation they have had.
            // NAMED ONLY ON TRUST (Jafar, 29 September page): Sheila keeps him
            // at "the new owner", her "new management", until the game says she
            // trusts him, whatever name its ladder sends; what it said holds
            // until it says otherwise (the independent check).
            // WHAT THEY CALL HIM, BY KNOWING (town list 6ch, carried until Jafar
            // rules): when the game sends no name, from what they know of his:
            // told in this talk, the street's fact the game says they hold, or
            // Mickey's own people; Tom after two days' talk or when he asks.
            void LearnsName(int from)
            {
                if (engine.NameKnownFrom < 0 || from < engine.NameKnownFrom) engine.NameKnownFrom = from;
                engine.KnowsHisName = true;
            }
            if (!string.IsNullOrEmpty(say))
            {
                var (gave, askedFirst) = PlayerIdentity.GivesName(say);
                if (gave) { LearnsName(day); gaveNameOut = true; }
                if (askedFirst) engine.AskedFirstName = true;
            }
            // Mickey's own knew it before he came (every day of talk counts); the
            // street's fact from today.
            if (Cast != null && PlayerIdentity.MickeysOwn.Contains(key)) LearnsName(0);
            else if (knowsNameSent && !engine.KnowsHisName) LearnsName(day);
            // A name the game sends is theirs from then on, never back down (the
            // third review: the next line without one fell to "the new owner").
            if (callsHim != null && Tom.RungOf(callsHim) is PlayerIdentity.Rung sentRung)
            {
                if (sentRung >= PlayerIdentity.Rung.Surname && !engine.KnowsHisName) LearnsName(day);
                if (sentRung > engine.GameRung) engine.GameRung = sentRung;
                if (sentRung > engine.CallsRung) engine.CallsRung = sentRung;
            }
            engine.CallsRung = PlayerIdentity.RungByKnowing(engine.KnowsHisName, engine.DaysTalkedKnowingHim, engine.AskedFirstName, engine.CallsRung);
            callsSentByGame = callsHim != null;
            if (callsHim == null) callsHim = Tom.CallsFor(engine.CallsRung);
            if (trustsSent.HasValue) lock (_trusts) _trusts[key] = trustsSent.Value;
            bool trustsHim = TrustsHim(key, engine);
            if (!trustsHim && Cast != null && Cast.NamesHimOnlyOnTrust(key)) callsHim = null;
            if (acquaintanceSent)
            {
                engine.HowYouKnowHim = Tom.HowTheyKnowHim(metHim || engine.HasSpokenWithHim, heardOfHim, callsHim, onlyTheirOwnTalk: !metHim);
                engine.KnowsHimFromGame = true;
            }
            else if (!engine.KnowsHimFromGame)
                engine.HowYouKnowHim = Tom.HowTheyKnowHim(engine.HasSpokenWithHim, false, callsHim, onlyTheirOwnTalk: true);
            // WHAT THEY HAVE HEARD OF HIS NIGHTS, as the street's rule counts it
            // (StreetVoice.RegardFor), 28 September; kept until the game sends
            // it again, "nothing" included.
            if (knowingSent) { engine.Heard = knowing; engine.HeardStory = knowingStory; }
            if (derived.HasValue)
            {
                suspicion = derived.Value.value;
                suspicionWhy = derived.Value.why;
            }
            // HIS ANSWER ABOUT WHERE HE WAS (town list 6ac): only an answer to their
            // own question of where he was, read from plain statements, checked
            // against where they saw him at about the deed's time, by area.
            object claimOut = null;
            if (deedTopic != null) engine.CurrentDeed = deedTopic;
            // What his answers about this deed weigh before this turn: without the
            // game's evidence only the change moves them (the independent check of 6am).
            double answersBefore = engine.AnswerWeight(deedTopic);
            string AreaWords(string area) => area == null || Cast == null ? null : Cast.AreaNames(area) is var nm && nm.Count > 0 ? nm[0] : area;
            string deedSawArea = Cast?.AreaFor(sawHimAt);
            // WHAT THEY SAW OR HEARD OF WHERE HE WAS, for trust (town list 6bz).
            if (deedTopic != null && Cast != null && (deedSawArea != null || Cast.AreaFor(heardHimAt) != null)) engine.NoteEvidence(deedTopic);
            // Seen or heard of near a deed where no place could be named (the
            // independent check: a sighting more than a few metres from any
            // place of the cast's came with no sawHimAt, and counted for nothing).
            if (sawHimNear) engine.NoteEvidence(deedTopic ?? "near");
            // A LIE FOUND OUT LATER (town list 6am), first: an answer they could not
            // judge, judged again once they know where he was, before anything he
            // says now can replace it (the independent check: a changed story
            // escaped). A list or vague answer is never a lie; if they saw him
            // somewhere it does not name, they say so.
            if (deedTopic != null && Cast != null && deedSawArea != null)
            {
                var held = engine.Answers.Find(x => x.Topic == deedTopic);
                if (held != null && held.Result == ClaimResult.Unknown)
                {
                    bool fitsHeld = false;
                    foreach (var ar in held.Areas) if (Cast.Fits(ar, deedSawArea)) fitsHeld = true;
                    if (held.Definite)
                    {
                        var later = fitsHeld ? ClaimResult.Consistent : ClaimResult.Contradiction;
                        if (engine.JudgeAgain(deedTopic, later, AreaWords(deedSawArea), now))
                            claimOut = new { topic = deedTopic, areas = held.Areas, result = later.ToString().ToLowerInvariant(), definite = true, later = true };
                    }
                    else if (!fitsHeld) engine.SawOtherwise(deedTopic, AreaWords(deedSawArea), now);
                }
            }
            var deedWhen = new Claims.DeedWhen(deedDay, deedHour, now.Day);
            if (deedTopic != null && Cast != null && !string.IsNullOrEmpty(say) && engine.AskedWhereAbout(deedWhen, out bool looseQuestion))
            {
                var areas = Claims.WhereHeSays(say, Cast.SpokenAreas(), deedWhen, true, out bool definite);
                // A question about a whole day leaves any answer at most unknown.
                if (looseQuestion) definite = false;
                // Only a known place or area is a sighting; only a definite answer
                // checks out or is caught. Any other is unknown when it could be true,
                // and not taken down at all when nothing in it fits what they saw:
                // "you cannot say otherwise" would be untrue (the fourth pass).
                string sawArea = areas.Count > 0 ? Cast.AreaFor(sawHimAt) : null;
                bool fits = false;
                foreach (var ar in areas) if (Cast.Fits(ar, sawArea)) fits = true;
                ClaimResult? judged = areas.Count == 0 ? (ClaimResult?)null
                    : sawArea == null ? ClaimResult.Unknown
                    : definite ? (fits ? ClaimResult.Consistent : ClaimResult.Contradiction)
                    : fits ? ClaimResult.Unknown : (ClaimResult?)null;
                if (judged.HasValue)
                {
                    var result = judged.Value;
                    var saidNames = new List<string>();
                    foreach (var ar in areas) { var n = Cast.AreaNames(ar); saidNames.Add(n.Count > 0 ? n[0] : ar); }
                    saidNames.Sort(StringComparer.Ordinal);
                    string sawWords = sawArea == null ? null : Cast.AreaNames(sawArea) is var sn && sn.Count > 0 ? sn[0] : sawArea;
                    engine.HeardAnswer(deedTopic, deedDay, deedHour, string.Join(" and ", saidNames), areas, result, sawWords, now, definite);
                    var areaList = new List<string>(areas); areaList.Sort(StringComparer.Ordinal);
                    // A lie caught later this same turn is what the game hears of, not the new story.
                    if (claimOut == null) claimOut = new { topic = deedTopic, areas = areaList, result = result.ToString().ToLowerInvariant(), definite, later = false };
                }
            }
            // HEARSAY, AND WHAT HE TOLD OTHERS (town list 6am), against the answer he
            // has now: hearsay against a definite answer is a doubt at half weight;
            // what he has been telling people, reaching somebody who saw him where
            // none of it fits, half a caught lie. The game sends both every turn.
            if (deedTopic != null && Cast != null)
            {
                var held = engine.Answers.Find(x => x.Topic == deedTopic);
                string heardArea = Cast.AreaFor(heardHimAt);
                if (held != null && heardArea != null)
                {
                    bool fitsHeard = false;
                    foreach (var ar in held.Areas) if (Cast.Fits(ar, heardArea)) fitsHeard = true;
                    if (!fitsHeard) engine.HeardOtherwise(deedTopic, AreaWords(heardArea), now);
                }
                var saidAreas = new List<string>();
                foreach (var h in heardHeSaid) { var ar = Cast.AreaFor(h); if (ar != null && !saidAreas.Contains(ar)) saidAreas.Add(ar); }
                if (saidAreas.Count > 0 && deedSawArea != null)
                {
                    bool anyFits = false;
                    foreach (var ar in saidAreas) if (Cast.Fits(ar, deedSawArea)) anyFits = true;
                    var saidWords = new List<string>();
                    foreach (var ar in saidAreas) { var w = AreaWords(ar); if (!saidWords.Contains(w)) saidWords.Add(w); }
                    saidWords.Sort(StringComparer.Ordinal);
                    if (!anyFits) engine.HeardHeToldOthers(deedTopic, deedDay, deedHour, string.Join(" and ", saidWords), AreaWords(deedSawArea), now);
                }
            }

            // OWNING UP, AND "KEEP IT TO YOURSELF" (town list 6al): about the deed they
            // suspect him of; the Core decides whether they keep it quiet.
            string ownedUpOut = null;
            object keepsQuietOut = null;
            // A THREAT TO KEEP QUIET (town list 6cd): never an ask for silence;
            // the Core remembers it and they are warier; the game files the story.
            string threatenedOut = null;
            // TELLING RON NO (town list 6bn), in two steps, since it ends Mickey's
            // arrangement for good: while tonight's ask stands, a line that sounds
            // like a no gets Ron's own plain question back in place of a reply,
            // and his plain yes to it within the hour is the no (the independent
            // check twice: free talk read alone took "The drivers want Sunday
            // off. Tell them no." and "Tell them no. Only messing." for a no).
            // Ron remembers it only once the game has answered the night
            // (Arrangement.HeardNo); this reply has it as tonight's line.
            bool refusedAsk = false, askPlainly = false;
            engine.Tonight = null;
            bool askedBefore;
            GameTime askedAt;
            // Any line to anybody clears the question (the independent check: a
            // "Yes." to somebody else's remark must not answer it), and only
            // Ron, who brought the ask, is read for it.
            lock (_askedNo) { askedBefore = _askedNo.TryGetValue(key, out askedAt); _askedNo.Clear(); }
            // His yes answers the question Ron put while the ask stood, even once
            // it has lapsed (the independent review of 30 September, B4a: a yes at
            // two past one to a question at two to one was lost); the game is told
            // when the question was put (refusedAt) and answers that night as of then.
            object refusedAtOut = null;
            if ((askTonight || askedBefore) && key == Arrangement.Doorman && !string.IsNullOrEmpty(say))
            {
                // Within three game hours, not at them (the second independent check).
                bool asked = askedBefore && now.TotalMinutes - askedAt.TotalMinutes < 180 && now.TotalMinutes >= askedAt.TotalMinutes;
                if (asked && Arrangement.ConfirmsNo(say))
                {
                    refusedAsk = true;
                    refusedAtOut = new { day = askedAt.Day, hour = askedAt.Hour, minute = askedAt.Minute };
                }
                // Not asked again straight after: "No thanks." to his question is
                // a no to telling them, and must not bring the question back.
                else if (askTonight && !asked && Arrangement.SoundsLikeNo(say))
                {
                    askPlainly = true;
                    lock (_askedNo) _askedNo[key] = now;
                }
                if (askTonight || refusedAsk)
                    engine.Tonight = refusedAsk ? Arrangement.TonightToldNo : asked ? Arrangement.TonightNotYes : Arrangement.TonightAsked;
            }
            // THE WEEK'S END (town list 6ca): her question put in her own fixed
            // words; while it stands, a line that sounds like one answer gets her
            // plain question back, and his plain yes to it, as his very next
            // line to her, is his answer (WeeksEnd.Sounds, Confirms), as his no
            // to Ron is read. Her lines here are fixed, so they need no model.
            string weekReply = null, weekDeal = null;
            WeekAnswer weekAnswer = WeekAnswer.None;
            // Trust is never earned while her question stands: she put it over
            // the book her trust had decided, and says so (the independent
            // check: the day-book's "the other one stays where it is" came with
            // trustEarned, the game's cue for the real book).
            if (key == WeeksEnd.Sheila && (weekAsk || weekStands)) engine.WeekDay = day;
            bool weekOpen = key == WeeksEnd.Sheila && engine.WeekDay == day;
            WeekAnswer weekAsked;
            bool weekAskedBefore;
            lock (_askedNo) { weekAskedBefore = _askedWeek.TryGetValue(key, out weekAsked); _askedWeek.Clear(); }
            if (key == WeeksEnd.Sheila && !string.IsNullOrEmpty(say))
            {
                if (weekAsk)
                    weekReply = WeeksEnd.Opening(weekRealBook, weekDayOff);
                else if (weekStands)
                {
                    if (weekAskedBefore && WeeksEnd.Confirms(say, weekAsked))
                    {
                        weekAnswer = weekAsked;
                        weekReply = WeeksEnd.Took(weekAsked);
                    }
                    // A clear answer, even with her plain question still waiting
                    // for another, gets the plain question for this one (the
                    // independent check: "I'm taking it over." after "Wind it
                    // down, then?" was never read).
                    else if (WeeksEnd.Sounds(say) is var sounds && sounds != WeekAnswer.None)
                    {
                        weekReply = WeeksEnd.AskPlainly(sounds, weekEnded);
                        // Which deal's plain question this is, so the game offers its yes and no.
                        weekDeal = "sheila-week-" + sounds.ToString().ToLowerInvariant();
                        lock (_askedNo) _askedWeek[key] = sounds;
                    }
                    // With talk off, the question again, never a brush-off.
                    else if (_llm == null) weekReply = WeeksEnd.StillAsks;
                    else engine.Tonight = WeeksEnd.StandingLine(weekRealBook);
                }
            }
            // Only the deed this line is sent with: an older deed would come without
            // its gravity (the independent check: a killing kept quiet).
            string silenceTopic = deedTopic;
            if (silenceTopic != null && !string.IsNullOrEmpty(say))
            {
                if (Silence.OwnsUp(say) && engine.HeardOwnUp(silenceTopic, now)) ownedUpOut = silenceTopic;
                if (Silence.Threatens(say) && engine.HeardThreat(silenceTopic, now)) threatenedOut = silenceTopic;
                // Any menace at all over it: no later ask buys silence, and her
                // own promise of it is caught (the fifth review of 6cd).
                else if (Silence.Menaces(say)) engine.Menaced.Add(silenceTopic);
                if (Silence.AsksQuiet(say))
                {
                    var stance = Cast?.QuietStance(key) ?? KeepsQuietFor.Friend;
                    var ident = new PlayerIdentity();
                    // First-name terms earned, never merely asked for (the independent
                    // check of 6ch: "Call me Tom." on a first meeting bought a friend's silence).
                    bool firstName = callsHim != null && (callsHim == ident.First || callsHim == ident.Diminutive)
                                     && (callsSentByGame || engine.GameRung >= PlayerIdentity.Rung.First || engine.DaysTalkedKnowingHim >= 2);
                    // Never for a man who has threatened them over it (the third
                    // review of 6cd: the threat on one line, the ask on the next).
                    engine.HeardAskQuiet(silenceTopic, Silence.Agrees(stance, firstName, deedGrave) && !engine.Menaced.Contains(silenceTopic), now);
                    bool agreed = engine.KeepsQuiet[silenceTopic];
                    keepsQuietOut = new { topic = silenceTopic, agreed, fragile = agreed && Silence.Fragile(stance) };
                }
            }
            // A THREAT THE WORDS MISSED, READ BY THE CHECKING MODEL (Jafar, 30
            // September, on his page: "the checking model reads each line about a
            // deed for a threat", on the capped key while he plays). Beside the
            // reply, never before it, so the reply waits no longer; waited on
            // before the turn's answer is written, ThreatWait at most. Found, it
            // is a threat as one the words found is, for the game and every later
            // turn; this turn's reply was already on its way without it.
            Task<LlmResponse> threatRead = null;
            if (ThreatByModel && _llm != null && silenceTopic != null && threatenedOut == null && !string.IsNullOrWhiteSpace(say))
            {
                try { threatRead = _llm.CompleteAsync(ThreatRead.Ask(engine.CheckerModel, say), CancellationToken.None); }
                catch (Exception) { threatRead = null; }
            }
            async Task ThreatReadDone()
            {
                var t = threatRead;
                threatRead = null;
                if (t == null) return;
                if (await Task.WhenAny(t, Task.Delay(ThreatWait)) != t || t.Status != TaskStatus.RanToCompletion || t.Result == null) return;
                _cost?.Record(engine.CheckerModel, t.Result.InputTokens, t.Result.OutputTokens);
                if (ThreatRead.Parse(t.Result.Text) == true && engine.HeardThreat(silenceTopic, now)) threatenedOut = silenceTopic;
            }
            if (suspicion.HasValue)
            {
                // THE REASON CARRIES THE MOVE, so it reads as the reason the
                // level is where it is (LatestReason takes only raising ones).
                if (string.IsNullOrEmpty(suspicionWhy)) engine.Suspicion.Restore(suspicion.Value);
                else { engine.Suspicion.Restore(0.0); engine.Suspicion.Raise(suspicion.Value, suspicionWhy); }
                // And what he has told them about this deed, on top, every turn the evidence is set.
                engine.ApplyAnswers(engine.CurrentDeed);
            }
            else if (deedTopic != null)
            {
                // No evidence this turn: only the change in what his answers weigh
                // moves them, once.
                double change = engine.AnswerWeight(deedTopic) - answersBefore;
                if (change > 1e-12) engine.Suspicion.Raise(change, engine.AnswerReason(deedTopic));
                else if (change < -1e-12) engine.Suspicion.Lower(-change, "his story fits what I saw");
            }
            string level = engine.Suspicion.Level.ToString();
            double holds = Math.Round(engine.Suspicion.Value, 3);
            // The manner a story gave them, when it did (null otherwise).
            string manner = engine.HeardManner() == null ? null : engine.Heard == Knowing.ALittle ? "little" : "enough";
            var heard = new List<string>();
            foreach (var m in MemoryRetrieval.Retrieve(engine.Memory, say, now)) heard.Add(m.Text);

            if (weekReply != null)
            {
                await ThreatReadDone();
                // Sheila's own fixed words, in place of a reply: no model writes them.
                engine.RememberSaid(say, weekReply, now);
                var (wTrusts, wEarned) = TrustAfter(key, engine, day, canEarn: !weekOpen);
                return JsonSerializer.Serialize(new { id, to, day, reply = weekReply, ms = sw.ElapsedMilliseconds, offline = _llm == null, timedOut = false, heard, suspicion = holds, level, why = suspicionWhy ?? engine.Suspicion.LatestReason(), manner, went = "own", claim = claimOut, ownedUp = ownedUpOut, threatened = threatenedOut, keepsQuiet = keepsQuietOut, refusedAsk, refusedAt = refusedAtOut, generated = false, calls = callsHim ?? Tom.Unplaced, gaveName = gaveNameOut, trusts = wTrusts, trustEarned = wEarned, weekAnswer = weekAnswer == WeekAnswer.None ? null : weekAnswer.ToString(), deal = weekDeal }, Plain);
            }
            if (askPlainly)
            {
                // Ron's own question, in place of a reply: no model writes it.
                engine.RememberSaid(say, Arrangement.AskPlainly, now);
                await ThreatReadDone();
                return JsonSerializer.Serialize(new { id, to, day, reply = Arrangement.AskPlainly, deal = "ron-tell-them-no", ms = sw.ElapsedMilliseconds, offline = false, timedOut = false, heard, suspicion = holds, level, why = suspicionWhy ?? engine.Suspicion.LatestReason(), manner, went = "own", claim = claimOut, ownedUp = ownedUpOut, threatened = threatenedOut, keepsQuiet = keepsQuietOut, refusedAsk, refusedAt = refusedAtOut, generated = false, calls = callsHim ?? Tom.Unplaced, gaveName = gaveNameOut }, Plain);
            }
            if (refusedAsk && _llm != null)
            {
                // His no confirmed: Ron's own acknowledgement, a moment that matters,
                // so no model writes it, live or stand-in (the builder's report of 30
                // September: the stand-in answered with a memory line).
                engine.RememberSaid(say, Arrangement.TookNo, now);
                await ThreatReadDone();
                return JsonSerializer.Serialize(new { id, to, day, reply = Arrangement.TookNo, ms = sw.ElapsedMilliseconds, offline = false, timedOut = false, heard, suspicion = holds, level, why = suspicionWhy ?? engine.Suspicion.LatestReason(), manner, went = "own", claim = claimOut, ownedUp = ownedUpOut, threatened = threatenedOut, keepsQuiet = keepsQuietOut, refusedAsk, refusedAt = refusedAtOut, generated = false, calls = callsHim ?? Tom.Unplaced, gaveName = gaveNameOut }, Plain);
            }
            if (_llm == null)
            {
                var (offTrusts, offEarned) = TrustAfter(key, engine, day, canEarn: !weekOpen);
                return JsonSerializer.Serialize(new { id, to, day, reply = refusedAsk ? Arrangement.TookNo : brush, ms = 0L, offline = true, timedOut = false, paused = AiNotice.TalkOff, heard, suspicion = holds, level, why = suspicionWhy ?? engine.Suspicion.LatestReason(), manner, ownedUp = ownedUpOut, threatened = threatenedOut, keepsQuiet = keepsQuietOut, refusedAsk, refusedAt = refusedAtOut, trusts = offTrusts, trustEarned = offEarned, calls = callsHim ?? Tom.Unplaced, gaveName = gaveNameOut }, Plain);
            }
            string reply;
            string paused = null;
            bool timedOut = false;
            string earlyFirst = null;
            var gate = new object();
            bool closed = false;
            if (_unwinding.TryGetValue(engine, out var before))
            {
                await Task.WhenAny(before, Task.Delay(10000));
                _unwinding.Remove(engine);
            }
            using var walkCts = new CancellationTokenSource();
            _walkCts[key] = walkCts;
            try
            {
            // With the rest's own limit, a second beyond it, so the turn is cut by
            // the wait below (and recorded "cut"), never by the token racing it.
            using (var cts = new CancellationTokenSource(Early ? _patience + RestPatience + TimeSpan.FromSeconds(1) : _patience))
            {
                try
                {
                    Func<string, Task<bool>> onFirst = null;
                    engine.OnFirstWritten = Early && Pending
                        ? (Action<string>)(ahead =>
                        {
                            lock (gate)
                            {
                                if (closed) return;
                                Emit(JsonSerializer.Serialize(new { id, to, pending = ahead, ms = sw.ElapsedMilliseconds }, Plain));
                            }
                        })
                        : null;
                    if (Early)
                    {
                        onFirst = first =>
                        {
                            // Once this line's answer is written, a late first sentence is dropped.
                            lock (gate)
                            {
                                if (closed) return Task.FromResult(false);
                                // THE CONTENT RULE on the sentence itself: one the
                                // validator would replace is not said early; the turn
                                // goes on as if nothing had been (the independent check).
                                var said = ResponseValidator.Validate(first, card.Name, card.AlsoCalled);
                                if (ResponseValidator.IsDeflection(said, card.Name)) return Task.FromResult(false);
                                earlyFirst = said;
                                Emit(JsonSerializer.Serialize(new { id, to, first = earlyFirst, ms = sw.ElapsedMilliseconds, generated = true }, Plain));
                            }
                            return Task.FromResult(true);
                        };
                    }
                    // THE MODEL BY THE KIND OF MOMENT, NEVER BY WHO (Jafar's ruling D48):
                    // real conversation when the game says so, or a deed, evidence or a
                    // deal is standing, or it is a newcomer's real question; else small talk.
                    bool dealStanding = askTonight || weekAsk || weekStands;
                    lock (_askedNo) if (_askedNo.ContainsKey(to) || _askedWeek.ContainsKey(to) || _askedNo.ContainsKey(key) || _askedWeek.ContainsKey(key)) dealStanding = true;
                    engine.Model = TalkMoment.ModelFor(TalkMoment.Of(say, deedTopic != null || evidenceSent, dealStanding, momentSaid));
                    var task = engine.SayToAsync(say, now, scene, cts.Token, onFirst);
                    var walkedOff = Task.Delay(Timeout.Infinite, walkCts.Token).ContinueWith(_ => { }, TaskScheduler.Default);
                    var timeout = Task.Delay(_patience);
                    var done = await Task.WhenAny(task, timeout, walkedOff);
                    // The first sentence heard: the rest has its own limit.
                    if (done == timeout)
                    {
                        bool heardFirst;
                        lock (gate) heardFirst = earlyFirst != null;
                        if (heardFirst)
                        {
                            var more = Task.Delay(RestPatience);
                            done = await Task.WhenAny(task, more, walkedOff);
                            if (done == more) done = timeout;
                        }
                    }
                    if (done == walkedOff)
                    {
                        // HE WALKED OFF (town list 6ay): the reply stops, and they keep
                        // only what he heard, as town list 6v has it.
                        lock (gate) closed = true;
                        cts.Cancel();
                        await Task.WhenAny(task, Task.Delay(3000));
                        if (!task.IsCompleted) _unwinding[engine] = task;
                        string heardNow = _walkHeard.TryRemove(key, out var hn) ? hn : "";
                        if (task.Status != TaskStatus.RanToCompletion && earlyFirst == null) engine.RememberSaid(say, "...", now);
                        engine.WalkedAway(heardNow, now);
                        lock (_walkedHandled) _walkedHandled.Add(key);
                        // What his line did stands although the reply stopped: the
                        // game still answers a no, an owning up or an ask for silence.
                        await ThreatReadDone();
                        return JsonSerializer.Serialize(new { id, to, walkedOff = true, ownedUp = ownedUpOut, threatened = threatenedOut, keepsQuiet = keepsQuietOut, refusedAsk, refusedAt = refusedAtOut, gaveName = gaveNameOut }, Plain);
                    }
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
                        // (A first sentence already heard is kept by the engine itself
                        // as it unwinds: ConversationEngine.RememberSaid.)
                        await Task.WhenAny(task, Task.Delay(1000));
                        if (!task.IsCompleted) _unwinding[engine] = task;
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
                catch (LlmApiException e) when (AiNotice.TalkPaused(e.ErrorType, e.Until) != null)
                {
                    // THE RELAY SAID NO (town list 6t): the character still brushes him
                    // off, and the player is told why and when talk comes back.
                    reply = brush;
                    paused = AiNotice.TalkPaused(e.ErrorType, e.Until);
                }
                catch (Exception)
                {
                    // ANY OTHER FAILURE (town list 6ax): still the brush-off, and now
                    // the player is told talk cannot be reached, not left to guess.
                    timedOut = true;
                    reply = brush;
                    paused = AiNotice.TalkUnreachable;
                }
            }
            }
            finally { _walkCts.TryRemove(key, out _); }
            // A no confirmed while talk is paused, unreachable or too slow gets
            // Ron's own acknowledgement, not a brush-off (the independent check).
            if (refusedAsk && (timedOut || paused != null) && earlyFirst == null) reply = Arrangement.TookNo;
            // INVENTED: what the first draft claimed that nothing supports, kept
            // for the log (the line said is the second draft or the plain one).
            // UNCHECKED: the claim check failed or answered out of shape, so the
            // line was said as written; apart from a clean check in the log.
            var invented = timedOut ? new List<string>() : new List<string>(engine.LastInvented);
            // PROMISED: what the first draft promised that the world will not keep (town list 6af), for the log.
            var promised = timedOut ? new List<string>() : new List<string>(engine.LastPromised);
            // SPOKE OF: the stories this reply drew on (town list 6ah), for the session record.
            var spokeOf = timedOut ? new List<string>() : new List<string>(engine.LastSpokeOf);
            // PUT TO HIS FACE (town list 6bc): the deed they raised with him, in their own words.
            var putToHim = timedOut || reply == brush ? new List<string>() : new List<string>(engine.LastPutToHim);
            // WHOM HIS LINE NAMED (town list 6bd), as cast ids, never the words.
            var named = Cast?.WhoNamed(say) ?? new List<string>();
            // HOW THE REPLY WENT (town list 6bd), for the session record's `reply` line:
            // where a friend's talk broke, beside the "still" it may explain.
            string went = paused != null ? "paused"
                : timedOut && earlyFirst != null ? "cut"
                : timedOut ? "brush"
                : ClaimCheck.IsKnownOnly(reply, card) ? "fallback"
                : ResponseValidator.IsDeflection(reply, card.Name) ? "refused"
                : (!timedOut && engine.LastEnded) ? "ended"
                : "own";
            bool @unchecked = !timedOut && engine.Checker != null && engine.LastUnchecked;
            // THE REST, when the first sentence has already been sent to be spoken:
            // what follows it, or nothing if the reply is no longer its sequel
            // (a brush-off after a timeout, or the first sentence alone).
            lock (gate) closed = true;
            string rest = null;
            if (earlyFirst != null)
            {
                int at = timedOut ? -1 : reply.IndexOf(earlyFirst, StringComparison.Ordinal);
                // (a dash the validator turned into a comma leaves the rest starting with one)
                rest = at >= 0 ? reply.Substring(at + earlyFirst.Length).Trim().TrimStart(',', ';', ':').Trim() : "";
                if (at < 0) reply = earlyFirst;
                // WHAT WAS HEARD is what the character keeps: the first sentence,
                // and the rest only if it is spoken (the independent check: a rest
                // the content rule refused stayed in memory unheard).
                if (!timedOut) engine.CorrectLastSaid(rest.Length > 0 ? earlyFirst + " " + rest : earlyFirst);
            }
            // FELL BACK: the reply is one of the "that's all I know" wordings,
            // for the log (how often the check leaves a character nothing to say).
            bool fellBack = !timedOut && ClaimCheck.IsKnownOnly(reply, card);
            // WRITTEN BY THE MODEL, marked so (the EU's AI Act, Article 50(2):
            // generated text marked in a form a machine can read); a brush-off
            // and the fallback line are the game's own words.
            // The chosen facts said plainly are built by code from written words.
            bool generated = reply != brush && !fellBack && !engine.LastSaidPlainly && !ResponseValidator.IsDeflection(reply, card.Name);
            string model = generated ? engine.Model : null;
            Keep(new Turn { Id = id, To = to, Day = day, Hour = hour, Minute = minute, Say = say, Reply = reply, Generated = generated,
                            Model = model, Invented = invented, Unchecked = @unchecked, Ms = sw.ElapsedMilliseconds });
            // ENDED: the character closed the conversation (town list 6ae).
            bool ends = !timedOut && engine.LastEnded;
            // THE TURN'S STEPS (town list 6bx), each with its milliseconds from the start.
            // Under the engine's own lock: a turn given up may still be marking steps as it unwinds.
            List<object[]> steps;
            lock (engine.LastSteps) steps = engine.LastSteps.ConvertAll(x => new object[] { x.step, x.ms });
            // TRUST EARNED (town list 6bz): for somebody who names him only on
            // trust, whether they trust him after this turn, and whether this
            // turn earned it; the game keeps it and sends it back.
            var (trusts, trustEarned) = TrustAfter(key, engine, day, canEarn: !weekOpen && (went == "own" || went == "ended" || went == "fallback"));
            await ThreatReadDone();
            return JsonSerializer.Serialize(new { id, to, day, reply, rest, ms = sw.ElapsedMilliseconds, offline = false, timedOut, paused, ends, heard, suspicion = holds, level, why = suspicionWhy ?? engine.Suspicion.LatestReason(), manner, invented, promised, spokeOf, putToHim, named, went, claim = claimOut, ownedUp = ownedUpOut, threatened = threatenedOut, keepsQuiet = keepsQuietOut, refusedAsk, refusedAt = refusedAtOut, @unchecked, fellBack, generated, model, steps, trusts, trustEarned, calls = callsHim ?? Tom.Unplaced, gaveName = gaveNameOut }, Plain);
        }

        static bool Bool(JsonElement e, string name) =>
            e.TryGetProperty(name, out var v) && v.ValueKind == JsonValueKind.True;
    }

    /// THE STAND-IN MODEL FOR THE ENCOUNTER'S REGRESSION: it answers from the
    /// memories its prompt was given and nothing else, so what the simulation
    /// knew is visible in the reply without a key or a bill.
    /// PROMPT SIZES (town list T1): each request, one JSON line: its model,
    /// its kind (the reply; the check's list of specifics, its second look, or
    /// its one-call check), whether it was streamed, and the characters of its
    /// system prompt and its messages. The stand-in underneath answers.
    sealed class SizeRecorder : IStreamingLlmClient
    {
        readonly ILlmClient _inner;
        readonly string _path;
        readonly object _gate = new object();
        public SizeRecorder(ILlmClient inner, string path) { _inner = inner; _path = path; }

        public static string Kind(LlmRequest r)
        {
            var sys = r.System ?? "";
            if (sys.Contains("list the specifics it states")) return "check-items";
            if (sys.StartsWith("You check details against", StringComparison.Ordinal)) return "check-verify";
            if (sys.Contains("check it against what they know")) return "check-line";
            return "reply";
        }

        void Log(LlmRequest r, bool streamed)
        {
            int messages = 0;
            foreach (var m in r.Messages) messages += m.Content?.Length ?? 0;
            var line = JsonSerializer.Serialize(new { model = r.Model, kind = Kind(r), streamed, system = r.System?.Length ?? 0, messages, turns = r.Messages.Count, maxTokens = r.MaxTokens });
            lock (_gate)
            {
                File.AppendAllText(_path, line + "\n");
                // The first request of each kind whole, to read what fills it.
                var whole = _path + "." + Kind(r) + "." + (r.Model ?? "model") + ".txt";
                if (!File.Exists(whole))
                {
                    var sb = new System.Text.StringBuilder("SYSTEM\n" + r.System + "\n");
                    foreach (var m in r.Messages) sb.Append("\n" + m.Role.ToUpperInvariant() + "\n" + m.Content + "\n");
                    File.WriteAllText(whole, sb.ToString());
                }
            }
        }

        public Task<LlmResponse> CompleteAsync(LlmRequest r, CancellationToken ct = default)
        {
            Log(r, false);
            return _inner.CompleteAsync(r, ct);
        }

        public async Task<LlmResponse> StreamAsync(LlmRequest r, Action<string> onText, CancellationToken ct = default)
        {
            Log(r, true);
            var resp = await _inner.CompleteAsync(r, ct);
            var text = resp.Text ?? "";
            for (int i = 8; i < text.Length + 8; i += 8) onText(text.Substring(0, Math.Min(text.Length, i)));
            return resp;
        }
    }

    /// The stand-in for the threat reading (ThreatRead): it answers the reading
    /// as told and counts it; anything else goes to the plain stand-in.
    sealed class ThreatFake : ILlmClient
    {
        readonly ILlmClient _rest = new FakeLlm();
        public bool Says;
        public int Reads;
        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            if ((request.System ?? "").Contains("threatens them to keep quiet"))
            {
                Interlocked.Increment(ref Reads);
                return Task.FromResult(new LlmResponse { Text = Says ? "{\"threat\": true}" : "{\"threat\": false}", Model = request.Model, InputTokens = 10, OutputTokens = 5 });
            }
            return _rest.CompleteAsync(request, ct);
        }
    }

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
            // A MANNER FROM A STORY (ConversationEngine.HeardManner): the stand-in
            // shows it the way the real model is asked to, cooler, without the
            // story, so a test can see the manner arrive.
            bool halfHeard = !suspects && sys.Contains("You have half heard something about this person");
            string text = halfHeard ? "Oh. It's you. I've heard bits." : first == null && why == null ? "Morning. Quiet one today."
                : suspects ? "I know what happened. " + (why ?? first) + " Was that you?"
                : "Funny business round here. " + first;
            return Task.FromResult(new LlmResponse { Text = text, StopReason = "end_turn", InputTokens = 400, OutputTokens = 20, Model = request.Model });
        }
    }

    static string CardsDir(string[] args)
    {
        for (int i = 0; i + 1 < args.Length; i++) if (args[i] == "--cards") return args[i + 1];
        // AS SHIPPED (town list 6aa): a "cards" folder beside the program, on a
        // friend's PC with no project folder anywhere; the project's own copy
        // when run from the repository.
        var beside = Path.Combine(AppContext.BaseDirectory, "cards");
        if (Directory.Exists(beside)) return beside;
        var d = new DirectoryInfo(AppContext.BaseDirectory);
        while (d != null)
        {
            var c = Path.Combine(d.FullName, "production", "cast", "cards");
            if (Directory.Exists(c)) return c;
            d = d.Parent;
        }
        return Path.Combine("production", "cast", "cards");
    }

    /// The named cast's file: beside the program as shipped, else the project's
    /// (production/specs/hook-cast.json, beside the cards).
    static void LoadCast(Helper h, string cardsDir)
    {
        var path = Path.Combine(AppContext.BaseDirectory, "hook-cast.json");
        if (!File.Exists(path)) path = Path.GetFullPath(Path.Combine(cardsDir, "..", "..", "specs", "hook-cast.json"));
        if (!File.Exists(path)) return;
        try { h.Cast = CastDay.Parse(File.ReadAllText(path)); } catch (FormatException) { h.Cast = null; }
    }

    /// Tom's written suggested lines: beside the program as shipped, else the
    /// project's (production/specs/suggested-lines.json, beside the cards).
    static void LoadSuggested(Helper h, string cardsDir)
    {
        var path = Path.Combine(AppContext.BaseDirectory, "suggested-lines.json");
        if (!File.Exists(path)) path = Path.GetFullPath(Path.Combine(cardsDir, "..", "..", "specs", "suggested-lines.json"));
        if (!File.Exists(path)) return;
        h.Written = Suggest.Written.Parse(File.ReadAllText(path));
    }

    static void LoadCards(Helper h, string dir)
    {
        if (!Directory.Exists(dir)) return;
        foreach (var f in Directory.GetFiles(dir, "*.md"))
        {
            var card = CharacterCard.Parse(File.ReadAllText(f));
            var key = Path.GetFileNameWithoutExtension(f).ToLowerInvariant();
            if (card == null) continue;
            // What the street knows that nobody had written (town list ck).
            h.Cards[key] = StreetFacts.AddTo(card, key);
        }
    }

    static async Task<int> Main(string[] args)
    {
        // THE FIRST-WEEK RULE TABLE AND THE PLAIN LINE, ON (Jafar's list of 30
        // September evening: on only if it cuts the empty answers without adding
        // inventions; measured on the sixty, a new sixty and thirty unanswerable,
        // production/research/grounded-replies/RULES-2026-09-30.md).
        ConversationEngine.UseRules = true;
        ConversationEngine.PlainFallback = true;
        if (Array.IndexOf(args, "--selftest") >= 0) return await SelfTest(CardsDir(args));
        var key = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY");
        bool fake = Array.IndexOf(args, "--fake") >= 0 || Environment.GetEnvironmentVariable("LEDGER_TALK_FAKE") == "1";
        // THROUGH OUR RELAY (town list 6b): --relay <address> and a copy's code
        // (--copy or LEDGER_COPY) instead of a key, so no key ships with the game.
        int ri = Array.IndexOf(args, "--relay"), ci = Array.IndexOf(args, "--copy");
        string relay = ri >= 0 && ri + 1 < args.Length ? args[ri + 1] : null;
        string copy = ci >= 0 && ci + 1 < args.Length ? args[ci + 1] : Environment.GetEnvironmentVariable("LEDGER_COPY");
        ILlmClient llm = fake ? new KnowledgeFake()
            : relay != null ? (string.IsNullOrEmpty(copy) ? null : new AnthropicClient(null) { BaseUrl = relay, CopyCode = copy })
            : (string.IsNullOrEmpty(key) ? null : new AnthropicClient(key));
        // WHAT IS SENT, MEASURED WITHOUT A KEY (town list T1): with the stand-in
        // and LEDGER_TALK_SIZES naming a file, every request is logged there and
        // the stand-in streams and checks as the real model would be asked to.
        string sizesPath = Environment.GetEnvironmentVariable("LEDGER_TALK_SIZES");
        bool sizes = fake && !string.IsNullOrEmpty(sizesPath);
        if (sizes) llm = new SizeRecorder(llm, sizesPath);
        // THE KEY'S CAP, ENFORCED IN CODE (Jafar, 30 September): with --budget-usd
        // (or LEDGER_TALK_BUDGET_USD) every call reserves its worst case first,
        // and none is sent that could take the run past the budget (BudgetedClient).
        int bi = Array.IndexOf(args, "--budget-usd");
        string budgetText = bi >= 0 && bi + 1 < args.Length ? args[bi + 1] : Environment.GetEnvironmentVariable("LEDGER_TALK_BUDGET_USD");
        if (llm != null && !fake && !string.IsNullOrEmpty(budgetText))
        {
            if (!double.TryParse(budgetText, System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out double budget) || !(budget >= 0))
            {
                Console.Error.WriteLine("talk: --budget-usd must be a number of dollars; refusing to start");
                return 2;
            }
            llm = new BudgetedClient(llm, budget);
        }
        var helper = new Helper(llm, TimeSpan.FromSeconds(8)) { CheckAlways = sizes };
        if (relay != null && !string.IsNullOrEmpty(copy))
        {
            // A player's report goes to our relay, which keeps it for us to act on.
            var reportClient = new System.Net.Http.HttpClient { Timeout = TimeSpan.FromSeconds(10) };
            helper.SendReport = async record =>
            {
                using var m = new System.Net.Http.HttpRequestMessage(System.Net.Http.HttpMethod.Post, relay.TrimEnd('/') + "/v1/report")
                    { Content = new System.Net.Http.StringContent(record, System.Text.Encoding.UTF8, "application/json") };
                m.Headers.Add("x-ledger-copy", copy);
                using var resp = await reportClient.SendAsync(m);
                return resp.IsSuccessStatusCode;
            };
        }
        helper.Early = Array.IndexOf(args, "--early") >= 0;
        helper.Pending = Array.IndexOf(args, "--pending") >= 0;
        LoadCards(helper, CardsDir(args));
        LoadCast(helper, CardsDir(args));
        LoadSuggested(helper, CardsDir(args));
        helper.Fake = fake;
        Console.Out.WriteLine(JsonSerializer.Serialize(new { ready = true, suggests = true, cards = helper.Cards.Keys, online = helper.Online, fake, notice = new { title = AiNotice.Title, text = AiNotice.TextFor(relay != null), report = AiNotice.ReportLabel } }, Plain));
        Console.Out.Flush();
        // Lines are still answered one at a time, in the order sent; but the
        // reader goes on reading while a reply is written, so a "walkedAway"
        // for the person being answered stops that reply at once (town list 6ay).
        var incoming = new System.Collections.Concurrent.BlockingCollection<string>();
        _ = Task.Run(() =>
        {
            string l;
            while ((l = Console.In.ReadLine()) != null) incoming.Add(l);
            incoming.CompleteAdding();
        });
        var waiting = new Queue<string>();
        // TOM'S SUGGESTED LINES OFF THE QUEUE (the builder, 1 October): a suggestion
        // reads only the talk so far, so it is answered beside the line being
        // answered, never in front of a spoken line sent just after it; its answer
        // is written when ready, every line out under one lock.
        var outLock = new object();
        var suggesting = new List<Task>();
        void Write(string json) { lock (outLock) { Console.Out.WriteLine(json); Console.Out.Flush(); } }
        void Suggest(string l) => suggesting.Add(Task.Run(async () => Write(await helper.Answer(l))));
        while (true)
        {
            string line;
            if (waiting.Count > 0) line = waiting.Dequeue();
            else if (!incoming.TryTake(out line, Timeout.Infinite)) break;
            if (line.Trim().Length == 0) continue;
            if (Helper.IsSuggest(line)) { Suggest(line); continue; }
            var answer = helper.Answer(line);
            while (!answer.IsCompleted)
            {
                if (incoming.TryTake(out var next, 50))
                {
                    if (Helper.IsSuggest(next)) { Suggest(next); continue; }
                    helper.WalkOffIfFor(next); waiting.Enqueue(next);
                }
                else if (incoming.IsCompleted) break;
            }
            Write(await answer);
        }
        await Task.WhenAll(suggesting);
        // WHAT THE SESSION COST, when the game closes the helper's input: the
        // calls, the tokens by model and the dollars at the game's own price
        // table - the measure Jafar asked for of an hour of play (23 September).
        Console.Out.WriteLine(JsonSerializer.Serialize(new
        {
            cost = helper.Cost.Report(),
            usd = helper.Cost.EstimateUsd(),
            calls = helper.Cost.TotalCalls,
            // Under a budget (--budget-usd): its spend with refused calls' reserves, and the calls it refused.
            budgetSpent = llm is BudgetedClient held ? held.SpentUsd : (double?)null,
            budgetRefused = llm is BudgetedClient refusing ? refusing.Refused : (int?)null,
        }, Plain));
        return 0;
    }

    // ---------------------------------------------------------------- the selftest, no network

    sealed class FakeLlm : ILlmClient
    {
        public string Next = "Hm. Is that so.";
        public TimeSpan Delay = TimeSpan.Zero;
        public int Calls;
        /// Every model asked, in order (the talk's model by the moment, D48).
        public readonly List<string> Seen = new List<string>();
        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            Calls++;
            lock (Seen) Seen.Add(request.Model);
            if (Delay > TimeSpan.Zero) await Task.Delay(Delay, ct);
            return new LlmResponse { Text = Next, StopReason = "end_turn", InputTokens = 400, OutputTokens = 20, Model = request.Model };
        }
    }

    // A stand-in model that says the next of its lines each call, then the last again.
    sealed class ScriptFake : ILlmClient
    {
        readonly Queue<string> _lines;
        string _last = "Right.";
        public ScriptFake(params string[] lines) => _lines = new Queue<string>(lines);
        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            // The threat reading (ThreatRead) is answered "no" and uses up no line of the script.
            if ((request.System ?? "").Contains("threatens them to keep quiet"))
                return Task.FromResult(new LlmResponse { Text = "{\"threat\": false}", StopReason = "end_turn", InputTokens = 100, OutputTokens = 5, Model = request.Model });
            if (_lines.Count > 0) _last = _lines.Dequeue();
            return Task.FromResult(new LlmResponse { Text = _last, StopReason = "end_turn", InputTokens = 400, OutputTokens = 20, Model = request.Model });
        }
    }

    sealed class BrokenFake : ILlmClient
    {
        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default) =>
            throw new LlmApiException(502, "The model could not be reached.", "upstream_unreachable", null);
    }

    sealed class RefusingFake : ILlmClient
    {
        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default) =>
            throw new LlmApiException(403, "This copy's allowance of live talk is spent for now.", "allowance_spent", "tomorrow");
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

        // THE CLAIM CHECK UNDER THE KEY'S SPENDING CAP (P3, 3 October; the rulings sweep of 1 October
        // and production/research/pre-production): a real model wrapped in the cap is still the real
        // model, so every reply it writes is checked, as Steam's disclosure promises; the stand-in,
        // capped or not, answers from memory only and is not.
        using (var real = new AnthropicClient("not-a-key-never-sent"))
        {
            Ok("the real model's replies are checked", Helper.ChecksReplies(real, false));
            Ok("the real model's replies are checked under the key's spending cap",
               Helper.ChecksReplies(new BudgetedClient(real, 1.0), false));
            Ok("the stand-in's are not, capped or not",
               !Helper.ChecksReplies(new KnowledgeFake(), false) && !Helper.ChecksReplies(new BudgetedClient(new KnowledgeFake(), 1.0), false));
        }

        // TOM'S SUGGESTED LINES (Jafar, 1 October): with the stand-in, his written
        // lines, three, none twice in the conversation; the model's own three
        // otherwise, from a call that never sees the card it would speak as.
        var sgh = new Helper(null, TimeSpan.FromSeconds(8)) { Fake = true };
        LoadCards(sgh, cardsDir);
        LoadSuggested(sgh, cardsDir);
        List<string> Suggested(string json)
        {
            var o = new List<string>();
            using var dj = JsonDocument.Parse(json);
            if (dj.RootElement.TryGetProperty("suggest", out var v) && v.ValueKind == JsonValueKind.Array)
                foreach (var el in v.EnumerateArray()) o.Add(el.GetString());
            return o;
        }
        var s1 = Suggested(await sgh.Answer("{\"kind\":\"suggest\",\"id\":11,\"to\":\"lena\",\"with\":\"Sheila\"}"));
        var s2 = Suggested(await sgh.Answer("{\"kind\":\"suggest\",\"id\":12,\"to\":\"lena\",\"with\":\"Sheila\"}"));
        var gaveG = new List<string>(sgh.Written.Greet); gaveG.RemoveAt(0);
        var shownJson = "[" + string.Join(",", gaveG.ConvertAll(x => JsonSerializer.Serialize(x))) + "]";
        var s3 = Suggested(await sgh.Answer("{\"kind\":\"suggest\",\"id\":15,\"to\":\"sam\",\"with\":\"Darren\",\"shown\":" + shownJson + "}"));
        Ok("only a suggest request is answered off the queue; a spoken line that says \"suggest\" is a spoken line",
           Helper.IsSuggest("{\"kind\":\"suggest\",\"id\":1,\"to\":\"lena\"}") && !Helper.IsSuggest("{\"id\":2,\"to\":\"lena\",\"say\":\"What do you \\\"suggest\\\"?\"}")
           && !Helper.IsSuggest("not json \"suggest\""));
        Ok("lines the game showed itself are never offered again in that conversation",
           s3.Count >= 2 && !s3.Exists(x => gaveG.Contains(x)) && s3[0] == sgh.Written.Greet[0], string.Join(" | ", s3));
        Ok("with the stand-in, three written lines, a greeting first, and none offered twice in one conversation",
           s1.Count == 3 && s2.Count == 3 && sgh.Written.Greet.Contains(s1[0]) && sgh.Written.Leave.Contains(s1[2]) && !s1.Exists(x => s2.Contains(x)),
           string.Join(" | ", s1) + " || " + string.Join(" | ", s2));
        var model = new FakeLlm { Next = "1. How do you mean, exactly?\n2. Do you like it here?\n3. I'll let you get on, then." };
        var sm = new Helper(model, TimeSpan.FromSeconds(8));
        LoadCards(sm, cardsDir);
        LoadSuggested(sm, cardsDir);
        await sm.Answer("{\"id\":13,\"to\":\"lena\",\"say\":\"Hello.\"}");
        int before = model.Calls;
        var sj = await sm.Answer("{\"kind\":\"suggest\",\"id\":14,\"to\":\"lena\",\"with\":\"Sheila\",\"tomKnows\":[\"Sheila Dunn keeps the books at Mickey's.\"]}");
        var sl = Suggested(sj);
        Ok("with a model, its three lines in their jobs, in one call of their own",
           sl.Count == 3 && sl[0] == "How do you mean, exactly?" && sl[2] == "I'll let you get on, then." && model.Calls == before + 1 && sj.Contains("\"generated\":[true,true,true]"), sj);

        var d = await h.Answer("not json");
        Ok("a broken line is refused, not guessed at", d.Contains("bad-line"), d);

        var off = new Helper(null, TimeSpan.FromSeconds(8));
        LoadCards(off, cardsDir);
        var e = await off.Answer("{\"id\":4,\"to\":\"lena\",\"say\":\"Got a minute?\"}");
        Ok("with the line down the character brushes the player off and says offline",
           Flag(e, "offline") && off.Cards["lena"].OwnWords["brush-off"].Contains(Reply(e)), e);

        var slow = new FakeLlm { Delay = TimeSpan.FromSeconds(2) };
        var s = new Helper(slow, TimeSpan.FromMilliseconds(300));
        LoadCards(s, cardsDir);
        var sw = Stopwatch.StartNew();
        var f = await s.Answer("{\"id\":5,\"to\":\"rocco\",\"say\":\"Alright?\"}");
        Ok("a slow model is abandoned for a brush-off at the patience limit",
           Flag(f, "timedOut") && s.Cards["rocco"].OwnWords["brush-off"].Contains(Reply(f)) && sw.ElapsedMilliseconds < 1800, f);
        await Task.Delay(2500);   // past the moment the abandoned reply would have landed
        int unheard = 0;
        foreach (var ev in s.EngineFor("rocco").Memory.Events) if (ev.Kind == "conversation") unheard++;
        Ok("an abandoned reply is cancelled, never remembered as said", unheard == 0, unheard.ToString());

        // THE SIMULATION'S STATE REACHES THE ANSWER, 24 September.
        // THE EVIDENCE IS ABOUT THE DEED THE LINE IS ABOUT (the independent review
        // of 1 October, N1, High): the game asked for the account under the scripted
        // story's key while the line's deed was the free play's, so a witness who saw
        // him was told, every line, that she held nothing. An account naming another
        // deed than the line's is not used: she stays as she was.
        string LevelOf(string json) { using var dj = JsonDocument.Parse(json); return dj.RootElement.TryGetProperty("level", out var lv) ? lv.GetString() : null; }
        var evH = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
        LoadCards(evH, cardsDir);
        string deedW = "\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23}";
        string sawIt = "\"evidence\":{\"account\":{\"topic\":\"player.window_d1\",\"held\":true,\"seen\":true,\"names\":true,\"rung\":4,\"confidence\":0.9,\"summary\":\"it was the new owner that put the window in\"},\"familiarity\":0.5}";
        string otherDeed = "\"evidence\":{\"account\":{\"topic\":\"player.broke_a_window\",\"held\":false,\"rung\":-1,\"confidence\":0},\"familiarity\":0.5}";
        var ev1 = await evH.Answer("{\"id\":301,\"to\":\"sam\",\"say\":\"Morning.\",\"day\":2,\"hour\":10,\"minute\":0," + sawIt + "," + deedW + "}");
        var ev2 = await evH.Answer("{\"id\":302,\"to\":\"sam\",\"say\":\"Busy?\",\"day\":2,\"hour\":10,\"minute\":1," + otherDeed + "," + deedW + "}");
        Ok("a witness who saw him stays as suspicious when a line's evidence is about another deed than the line's",
           LevelOf(ev1) != null && LevelOf(ev1) != "Trusting" && LevelOf(ev2) == LevelOf(ev1), ev1 + " || " + ev2);

        // THE MODEL FOLLOWS THE KIND OF MOMENT, NEVER WHO IS TALKING (Jafar's ruling D48,
        // again on 1 October): small talk on the lighter model for Sheila as for anybody;
        // a line with a deed standing, or a newcomer's real question, on the better one
        // for Ron and Darren as for anybody; and what the game says the moment is wins.
        var mf = new FakeLlm();
        var mh = new Helper(mf, TimeSpan.FromSeconds(8));
        LoadCards(mh, cardsDir);
        bool Asked(string model) { lock (mf.Seen) return mf.Seen.Contains(model); }
        mf.Seen.Clear(); await mh.Answer("{\"id\":401,\"to\":\"lena\",\"say\":\"Morning, Sheila.\"}");
        bool smallLight = mf.Seen.Count > 0 && !Asked(Models.Core);
        mf.Seen.Clear(); await mh.Answer("{\"id\":402,\"to\":\"rocco\",\"say\":\"Quiet night.\",\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23}}");
        bool deedBetter = Asked(Models.Core);
        mf.Seen.Clear(); await mh.Answer("{\"id\":403,\"to\":\"sam\",\"say\":\"Who runs things round here?\"}");
        bool questionBetter = Asked(Models.Core);
        mf.Seen.Clear(); await mh.Answer("{\"id\":404,\"to\":\"lena\",\"say\":\"Who runs things round here?\",\"moment\":\"smalltalk\"}");
        bool gameWord = mf.Seen.Count > 0 && !Asked(Models.Core);
        Ok("the talk's model follows the kind of moment, the same for everybody: small talk lighter, a deed or a real question better, the game's word first",
           smallLight && deedBetter && questionBetter && gameWord, $"{smallLight} {deedBetter} {questionBetter} {gameWord}");

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

        // KNOWING A LITTLE SHOWS IN TALK, 28 September.
        const string Little = "\"knowing\":{\"level\":\"little\",\"story\":\"the new owner was about the yard after midnight\"}";
        var faint = await q.Answer("{\"id\":12,\"to\":\"sam\",\"who\":\"f1\",\"say\":\"Morning.\",\"day\":5,\"hour\":10," + Little + "}");
        Ok("a person who knows a little is given the manner it gives them", Str(faint, "manner") == "little" && Str(faint, "level") == "Trusting", faint);
        Ok("and it shows in the answer", Reply(faint) == "Oh. It's you. I've heard bits.", faint);
        Ok("the manner is the story's, in the prompt, with no 'at ease'",
           q.EngineFor("f1").BuildSystemPrompt("Morning.", new GameTime(5, 10, 0), "").Contains("about the yard after midnight")
           && !q.EngineFor("f1").BuildSystemPrompt("Morning.", new GameTime(5, 10, 0), "").Contains("at ease with them"));
        var kept = await q.Answer("{\"id\":13,\"to\":\"sam\",\"who\":\"f1\",\"say\":\"Still here?\",\"day\":5,\"hour\":11}");
        Ok("kept until the game says otherwise", Str(kept, "manner") == "little", kept);
        var gone = await q.Answer("{\"id\":14,\"to\":\"sam\",\"who\":\"f1\",\"say\":\"Morning.\",\"day\":9,\"hour\":10,\"knowing\":{\"level\":\"nothing\"}}");
        Ok("and gone when the story is", Str(gone, "manner") == null && Reply(gone) != "Oh. It's you. I've heard bits.", gone);
        var both = await q.Answer("{\"id\":15,\"to\":\"sam\",\"who\":\"f2\",\"say\":\"Evening.\",\"day\":4,\"hour\":18," + Mem +
            ",\"evidence\":{" + Acc + ",\"near\":{\"sawHim\":true,\"others\":0,\"summary\":\"a man came through the yard at a run\"},\"familiarity\":0.2}," + Little + "}");
        Ok("a reason to suspect him outranks the manner: he asks", Str(both, "manner") == null && Str(both, "level") == "Suspicious" && Reply(both).Contains("?"), both);
        var unheard16 = await q.Answer("{\"id\":16,\"to\":\"sam\",\"who\":\"f3\",\"say\":\"Morning.\",\"day\":5,\"hour\":10}");
        Ok("somebody who has heard nothing has no manner from it", Str(unheard16, "manner") == null, unheard16);

        // THE FIRST SENTENCE, EARLY, 26 September: spoken as soon as it is
        // written and checked; never anything unchecked; kept as said.
        Ok("a first sentence is cut at its end", ConversationEngine.FirstSentence("Aye. I saw him.") == "Aye.");
        Ok("not until more follows it", ConversationEngine.FirstSentence("Aye.") == null && ConversationEngine.FirstSentence("Aye, I") == null);
        Ok("a title is not a sentence's end", ConversationEngine.FirstSentence("Mr. Hall knows. Ask him.") == "Mr. Hall knows.");
        Ok("a reply with a tag waits to be cleaned whole", ConversationEngine.FirstSentence("<thinking>Lie. </thinking> Aye. No.") == null);
        // The independent check's cases, 26 September.
        Ok("never inside a quotation", ConversationEngine.FirstSentence("He said \"Go home. Now.\" and walked off. That's all.") == "He said \"Go home. Now.\" and walked off.");
        Ok("never inside brackets", ConversationEngine.FirstSentence("Aye (I saw him. Honest) at nine. That's all.") == "Aye (I saw him. Honest) at nine.");
        Ok("\"No.\" before a number is not an end", ConversationEngine.FirstSentence("No. 12 had its window put in. Terrible.") == "No. 12 had its window put in.");
        Ok("\"No.\" before words is", ConversationEngine.FirstSentence("No. I never saw him.") == "No.");
        Ok("an initial is not an end", ConversationEngine.FirstSentence("It was J. Novak. I saw him.") == "It was J. Novak.");
        Ok("nor are a.m. and Sgt.", ConversationEngine.FirstSentence("About 9 a.m. he came. Ask Sgt. Hall. Go on.") == "About 9 a.m. he came.");
        Ok("dots alone are not a sentence", ConversationEngine.FirstSentence("... Right. Off you go.") == "... Right.");
        // The second attack's cases.
        Ok("never inside a single quotation", ConversationEngine.FirstSentence("He said 'Go home. Now.' and walked off. That's all.") == "He said 'Go home. Now.' and walked off.");
        Ok("nor after Capt.", ConversationEngine.FirstSentence("It was Capt. Hale. I saw him.") == "It was Capt. Hale.");
        Ok("a contraction ends a sentence", ConversationEngine.FirstSentence("No, I can't. Ask Rocco, he might.") == "No, I can't.");
        Ok("an apostrophe in a word opens nothing", ConversationEngine.FirstSentence("The lads' van was here. Then gone.") == "The lads' van was here.");
        Ok("nor does a dropped letter", ConversationEngine.FirstSentence("'Course I did. Saw him plain.") == "'Course I did." &&
           ConversationEngine.FirstSentence("I saw 'im. Plain as day.") == "I saw 'im.");

        async Task<(List<(long at, string line)> firsts, string last, long lastAt, StreamFake llm, Helper helper)> Early(StreamFake llm, string say, TimeSpan patience)
        {
            // The rest's own limit off here: these cases are about the turn's patience.
            var eh = new Helper(llm, patience) { Early = true, CheckAlways = true, RestPatience = TimeSpan.Zero };
            LoadCards(eh, cardsDir);
            var clock = Stopwatch.StartNew();
            var firsts = new List<(long, string)>();
            eh.Emit = line => { lock (firsts) firsts.Add((clock.ElapsedMilliseconds, line)); };
            var last = await eh.Answer("{\"id\":20,\"to\":\"sam\",\"say\":\"" + say + "\"}");
            return (firsts, last, clock.ElapsedMilliseconds, llm, eh);
        }
        string Said(Helper eh)
        {
            string o = null;
            foreach (var ev in eh.EngineFor("sam").Memory.Events)
                if (ev.Kind == "conversation" && ev.Text.StartsWith(ClaimCheck.IReplied)) o = ev.Text;
            return o;
        }

        // THE REST'S OWN LIMIT (town list 6bx): the first sentence heard before the
        // turn's patience, the rest comes in its own time; past that it is cut,
        // recorded "cut", never a brush-off.
        {
            var slowRest = new StreamFake("Aye. I saw him go by the chip shop at nine.") { Pause = TimeSpan.FromMilliseconds(1500) };
            var restHelper = new Helper(slowRest, TimeSpan.FromMilliseconds(1000)) { Early = true, CheckAlways = true, RestPatience = TimeSpan.FromSeconds(4) };
            LoadCards(restHelper, cardsDir);
            restHelper.Emit = _ => { };
            var within = await restHelper.Answer("{\"id\":21,\"to\":\"sam\",\"say\":\"See anything?\"}");
            var cutRest = new StreamFake("Aye. I saw him go by the chip shop at nine.") { Pause = TimeSpan.FromMilliseconds(3000) };
            var cutHelper = new Helper(cutRest, TimeSpan.FromMilliseconds(1000)) { Early = true, CheckAlways = true, RestPatience = TimeSpan.FromMilliseconds(500) };
            LoadCards(cutHelper, cardsDir);
            cutHelper.Emit = _ => { };
            var cutOff = await cutHelper.Answer("{\"id\":22,\"to\":\"sam\",\"say\":\"See anything?\"}");
            Ok("a rest slower than the turn's patience still comes when the first sentence was heard, within its own limit; past it the turn is cut after the first sentence, recorded as cut",
               Reply(within) == "Aye. I saw him go by the chip shop at nine." && within.Contains("\"went\":\"own\"") && within.Contains("[\"draft\",") && (within.Contains("[\"first-plain\",") || within.Contains("[\"first-passed\","))
               && Reply(cutOff) == "Aye." && cutOff.Contains("\"went\":\"cut\""), within + " | " + cutOff);
        }

        var clean = await Early(new StreamFake("Aye. I saw him go by the chip shop at nine."), "See anything?", TimeSpan.FromSeconds(8));
        Ok("the checked first sentence goes out before the rest is written",
           clean.firsts.Count == 1 && Str(clean.firsts[0].line, "first") == "Aye." && clean.firsts[0].at + 250 < clean.lastAt,
           clean.firsts.Count + " " + clean.lastAt);
        Ok("and the rest follows, to be spoken after it", Str(clean.last, "rest") == "I saw him go by the chip shop at nine." &&
           Reply(clean.last) == "Aye. I saw him go by the chip shop at nine.", clean.last);

        // THE FIRST SENTENCE AHEAD OF ITS CHECK (--pending; U1, 30 September):
        // written as "pending" the moment it is drafted, then as "first" once
        // it passes, the same words; one the check fails goes pending but never
        // first, so the game never plays it; one the content rule refuses is not
        // even pending; and without the flag nothing is written ahead.
        async Task<List<string>> Ahead(StreamFake llm, string say, bool pending = true)
        {
            var ah = new Helper(llm, TimeSpan.FromSeconds(8)) { Early = true, Pending = pending, CheckAlways = true, RestPatience = TimeSpan.Zero };
            LoadCards(ah, cardsDir);
            var lines = new List<string>();
            ah.Emit = line => { lock (lines) lines.Add(line); };
            lines.Add(await ah.Answer("{\"id\":23,\"to\":\"sam\",\"say\":\"" + say + "\"}"));
            return lines;
        }
        int At(List<string> lines, string key, string words) => lines.FindIndex(l => l.Contains("\"" + key + "\":\"" + words + "\""));
        var aheadClean = await Ahead(new StreamFake("Aye. I saw him go by the chip shop at nine."), "See anything?");
        Ok("with --pending the first sentence is written ahead of its check, then as first once it passes, the same words",
           At(aheadClean, "pending", "Aye.") >= 0 && At(aheadClean, "first", "Aye.") > At(aheadClean, "pending", "Aye."), string.Join(" | ", aheadClean));
        var aheadBad = await Ahead(new StreamFake("Dennis from the yard did it. Everyone knows."), "Who was it?");
        Ok("one its check fails is never written as first, so it is never played",
           aheadBad.TrueForAll(l => !l.Contains("\"first\":\"Dennis")), string.Join(" | ", aheadBad));
        var aheadPint = await Ahead(new StreamFake("Fancy a pint after? Aye."), "Busy?");
        var aheadOff = await Ahead(new StreamFake("Aye. I saw him go by the chip shop at nine."), "See anything?", pending: false);
        Ok("one the content rule refuses is not even written ahead, and without --pending nothing is",
           aheadPint.TrueForAll(l => !l.Contains("pint")) && aheadOff.TrueForAll(l => !l.Contains("\"pending\"")) && At(aheadOff, "first", "Aye.") >= 0,
           string.Join(" | ", aheadPint) + " || " + string.Join(" | ", aheadOff));

        var restBad = await Early(new StreamFake("Aye. It was Dennis from the yard, I know it."), "Who was it?", TimeSpan.FromSeconds(8));
        Ok("if the rest invents, only the checked first sentence is said",
           restBad.firsts.Count == 1 && Reply(restBad.last) == "Aye." && Str(restBad.last, "rest") == "", restBad.last);
        Ok("and remembered as all that was said", Said(restBad.helper) != null && Said(restBad.helper).Contains("\"Aye.\""), Said(restBad.helper));

        var restRefused = await Early(new StreamFake("Aye. Fancy a pint after?"), "Busy?", TimeSpan.FromSeconds(8));
        Ok("a rest the content rule refuses is not said", restRefused.firsts.Count == 1 && Reply(restRefused.last) == "Aye." && Str(restRefused.last, "rest") == "", restRefused.last);
        Ok("and is not kept as said either", Said(restRefused.helper) != null && !Said(restRefused.helper).Contains("pint"), Said(restRefused.helper));
        var bracket = await Early(new StreamFake("As an AI I would not know. Anyway, no."), "See anything?", TimeSpan.FromSeconds(8));
        Ok("a first sentence the validator would replace is not said early", bracket.firsts.Count == 0, bracket.last);

        var broke = await Early(new StreamFake("Aye. I saw him go by the chip shop at nine.") { ThrowBeforeText = true }, "See anything?", TimeSpan.FromSeconds(8));
        Ok("a stream that breaks before any sentence falls back to the plain call", broke.firsts.Count == 0 &&
           Reply(broke.last) == "Aye. I saw him go by the chip shop at nine." && !Flag(broke.last, "timedOut"), broke.last);
        var quoted = await Early(new StreamFake("Aye. \"Get out,\" he said. Then he went."), "What happened?", TimeSpan.FromSeconds(8));
        Ok("the rest keeps its own opening quote", Str(quoted.last, "rest") == "\"Get out,\" he said. Then he went.", quoted.last);

        var firstBad = await Early(new StreamFake("Dennis from the yard did it. Everyone knows."), "Who was it?", TimeSpan.FromSeconds(8));
        Ok("a first sentence that invents is never sent early", firstBad.firsts.Count == 0 && Str(firstBad.last, "rest") == null, firstBad.last);
        Ok("and the reply is the usual second draft or the plain line", Reply(firstBad.last) != null && !Reply(firstBad.last).Contains("Dennis"), firstBad.last);
        // Town list 6a: the failed draft is stopped, and the second draft's first
        // sentence goes out without waiting for the failed draft to finish.
        var redraftEarly = await Early(new StreamFake("Dennis from the yard did it. Everyone knows.") { Redraft = "Can't say I did. Ask Rita.", Pause = TimeSpan.FromSeconds(2) },
                                       "Who was it?", TimeSpan.FromSeconds(8));
        Ok("a first sentence that invents stops its draft, and the second draft's first sentence goes out at once",
           redraftEarly.llm.Stopped && redraftEarly.firsts.Count == 1 && Str(redraftEarly.firsts[0].line, "first") == "Can't say I did." && redraftEarly.firsts[0].at < 1500,
           redraftEarly.firsts.Count > 0 ? redraftEarly.firsts[0].at + " " + redraftEarly.firsts[0].line : redraftEarly.last);
        Ok("and its rest follows", Str(redraftEarly.last, "rest") == "Ask Rita." && Reply(redraftEarly.last) == "Can't say I did. Ask Rita.", redraftEarly.last);

        var late = await Early(new StreamFake("Aye. I saw him go by the chip shop at nine.") { Pause = TimeSpan.FromSeconds(3) }, "See anything?", TimeSpan.FromMilliseconds(900));
        Ok("out of time after the first sentence: that sentence is the reply, nothing more is said",
           late.firsts.Count == 1 && Flag(late.last, "timedOut") && Reply(late.last) == "Aye." && Str(late.last, "rest") == "", late.last);
        Ok("and the character keeps what the player heard", Said(late.helper) != null && Said(late.helper).Contains("\"Aye.\""), Said(late.helper));

        // A PLAYER'S REPORT (town list 6c), and every generated line marked as such.
        var reportsDir = Path.Combine(Path.GetTempPath(), "ledger-reports-selftest-" + Guid.NewGuid().ToString("N").Substring(0, 8));
        var rh = new Helper(new StreamFake("Aye. I saw him go by the chip shop at nine."), TimeSpan.FromSeconds(8)) { CheckAlways = true, ReportsDir = reportsDir };
        LoadCards(rh, cardsDir);
        var said30 = await rh.Answer("{\"id\":30,\"to\":\"sam\",\"say\":\"See anything?\"}");
        Ok("a line the model wrote is marked as generated, with its model", Flag(said30, "generated") && Str(said30, "model") != null, said30);
        var rep = await rh.Answer("{\"report\":30,\"why\":\"he named a stranger\"}");
        var keptReport = File.Exists(Path.Combine(reportsDir, "reports.jsonl")) ? File.ReadAllText(Path.Combine(reportsDir, "reports.jsonl")) : "";
        Ok("a reported line is kept with what was said, the reply and the player's note, and the answer says where and thanks them",
           Str(rep, "saved") == "local" && Flag(rep, "found") && keptReport.Contains("See anything?") && keptReport.Contains("chip shop") &&
           keptReport.Contains("he named a stranger") && Str(rep, "thanks") == AiNotice.ReportThanks("local"), rep + " / " + keptReport);
        Ok("a report of a line that never was finds nothing and keeps nothing",
           !Flag(await rh.Answer("{\"report\":999}"), "found") && File.ReadAllLines(Path.Combine(reportsDir, "reports.jsonl")).Length == 1);
        var sent = new List<string>();
        rh.SendReport = rec => { sent.Add(rec); return Task.FromResult(true); };
        Ok("with a relay, the report is sent there instead",
           Str(await rh.Answer("{\"report\":30}"), "saved") == "relay" && sent.Count == 1 && File.ReadAllLines(Path.Combine(reportsDir, "reports.jsonl")).Length == 1);
        rh.SendReport = rec => throw new InvalidOperationException("relay down");
        Ok("and when the relay cannot be reached it is kept here, never lost",
           Str(await rh.Answer("{\"report\":30}"), "saved") == "local" && File.ReadAllLines(Path.Combine(reportsDir, "reports.jsonl")).Length == 2);
        try { Directory.Delete(reportsDir, true); } catch (IOException) { }
        var slowHelper = new Helper(new StreamFake("I saw him go by the chip shop at nine and then some") { Pause = TimeSpan.FromSeconds(3) }, TimeSpan.FromMilliseconds(500)) { Early = true, CheckAlways = true };
        LoadCards(slowHelper, cardsDir);
        slowHelper.Emit = _ => { };
        var brushed = await slowHelper.Answer("{\"id\":31,\"to\":\"sam\",\"say\":\"See anything?\"}");
        Ok("a brush-off is the game's own words, not marked generated", Flag(brushed, "timedOut") && !Flag(brushed, "generated"), brushed);
        Ok("but a first sentence heard before time ran out is", Flag(late.last, "generated"), late.last);

        var plain = new Helper(new StreamFake("Aye. I saw him go by the chip shop at nine."), TimeSpan.FromSeconds(8)) { CheckAlways = true };
        LoadCards(plain, cardsDir);
        int plainFirsts = 0;
        plain.Emit = _ => plainFirsts++;
        var pl = await plain.Answer("{\"id\":21,\"to\":\"sam\",\"say\":\"See anything?\"}");
        Ok("without --early nothing changes: the whole reply, no first line, no rest",
           plainFirsts == 0 && Reply(pl) == "Aye. I saw him go by the chip shop at nine." && Str(pl, "rest") == null, pl);

        // HE WALKED OFF MID-REPLY (town list 6v).
        var walker = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
        LoadCards(walker, cardsDir);
        await walker.Answer("{\"id\":91,\"to\":\"sam\",\"say\":\"Seen anything?\"}");
        string walked = await walker.Answer("{\"walkedAway\":{\"to\":\"sam\",\"heard\":\"Hm.\"},\"day\":1,\"hour\":12}");
        var walkedEngine = walker.EngineFor("sam");
        Ok("walking off mid-reply: they keep only what he heard, and remember he left",
           walked.Contains("\"noted\":true") && walkedEngine.Memory.Events.Exists(e => e.Text.Contains("walked off while I was still talking"))
           && walkedEngine.Memory.Events.Exists(e => e.Text.EndsWith("\"Hm.\", and no more")), walked);

        // WHERE HE SAYS HE WAS (town list 6ac): an answer to their question, read
        // against where they saw him at the deed's time, and a lie kept on top.
        var alibi = new Helper(new FakeLlm { Next = "Where were you on Tuesday night, then?" }, TimeSpan.FromSeconds(8));
        LoadCards(alibi, cardsDir);
        LoadCast(alibi, cardsDir);
        string deedBits = "\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23,\"sawHimAt\":\"ritas_counter\"},\"suspicion\":0.5,\"suspicionWhy\":\"I saw him near the window\"";
        string unasked = await alibi.Answer("{\"id\":100,\"to\":\"sam\",\"say\":\"I was at the chapel all night.\",\"day\":2,\"hour\":10," + deedBits + "}");
        string lie = await alibi.Answer("{\"id\":101,\"to\":\"sam\",\"say\":\"I was at the chapel all night.\",\"day\":2,\"hour\":10," + deedBits + "}");
        string after = await alibi.Answer("{\"id\":102,\"to\":\"sam\",\"say\":\"Well?\",\"day\":2,\"hour\":10," + deedBits + "}");
        double Sus(string json) { using var d = JsonDocument.Parse(json); return d.RootElement.GetProperty("suspicion").GetDouble(); }
        Ok("an answer counts only once they have asked where he was; then a lie against what they saw keeps them more suspicious, turn after turn",
           !unasked.Contains("\"result\"") && lie.Contains("\"result\":\"contradiction\"") && Sus(lie) > 0.5 + 0.1 && Math.Abs(Sus(after) - Sus(lie)) < 1e-6
           && alibi.EngineFor("sam").BuildSystemPrompt("x", new GameTime(2, 10, 5), "").Contains("you saw him at Rita's"), unasked + " | " + lie);
        var truthful = new Helper(new FakeLlm { Next = "Where were you on Tuesday night, then?" }, TimeSpan.FromSeconds(8));
        LoadCards(truthful, cardsDir);
        LoadCast(truthful, cardsDir);
        await truthful.Answer("{\"id\":104,\"to\":\"sam\",\"say\":\"Evening.\",\"day\":2,\"hour\":10," + deedBits + "}");
        string truth = await truthful.Answer("{\"id\":105,\"to\":\"sam\",\"say\":\"I was at Rita\u2019s, then the chapel.\",\"day\":2,\"hour\":10," + deedBits + "}");
        Ok("a true answer naming where they saw him, among other places, is never a lie, nor lets him off", truth.Contains("\"result\":\"unknown\"") && Math.Abs(Sus(truth) - 0.5) < 1e-9, truth);
        var oddHelper = new Helper(new FakeLlm { Next = "Where were you on Tuesday night, then?" }, TimeSpan.FromSeconds(8));
        LoadCards(oddHelper, cardsDir);
        LoadCast(oddHelper, cardsDir);
        string oddBits = deedBits.Replace("ritas_counter", "quay_street");
        await oddHelper.Answer("{\"id\":106,\"to\":\"sam\",\"say\":\"Evening.\",\"day\":2,\"hour\":10," + oddBits + "}");
        string oddSaw = await oddHelper.Answer("{\"id\":107,\"to\":\"sam\",\"say\":\"I was at the chapel all night.\",\"day\":2,\"hour\":10," + oddBits + "}");
        Ok("a sighting the game names by no known place or area makes an answer unknown, never a lie", oddSaw.Contains("\"result\":\"unknown\""), oddSaw);
        var vague = new Helper(new FakeLlm { Next = "Where were you on Tuesday night, then?" }, TimeSpan.FromSeconds(8));
        LoadCards(vague, cardsDir);
        LoadCast(vague, cardsDir);
        await vague.Answer("{\"id\":108,\"to\":\"sam\",\"say\":\"Evening.\",\"day\":2,\"hour\":10," + deedBits + "}");
        string vagueSaid = await vague.Answer("{\"id\":109,\"to\":\"sam\",\"say\":\"I was at the chapel. Then the cafe.\",\"day\":2,\"hour\":10," + deedBits + "}");
        string meSaid = await alibi.Answer("{\"id\":110,\"to\":\"sam\",\"say\":\"Me? I was at the chapel all night.\",\"day\":2,\"hour\":10," + deedBits + "}");
        var dayQ = new Helper(new FakeLlm { Next = "Where were you yesterday?" }, TimeSpan.FromSeconds(8));
        LoadCards(dayQ, cardsDir);
        LoadCast(dayQ, cardsDir);
        await dayQ.Answer("{\"id\":111,\"to\":\"sam\",\"say\":\"Evening.\",\"day\":2,\"hour\":10," + deedBits + "}");
        string daySaid = await dayQ.Answer("{\"id\":112,\"to\":\"sam\",\"say\":\"I was at the cafe.\",\"day\":2,\"hour\":10," + deedBits + "}");
        Ok("asked about a whole day, his plain answer is never a lie", !daySaid.Contains("contradiction") && Math.Abs(Sus(daySaid) - 0.5) < 1e-9, daySaid);
        Ok("an answer that is not plain and names nowhere they saw him is not taken down at all; \"Me?\" before a plain answer leaves it plain",
           vagueSaid.Contains("\"claim\":null") && Math.Abs(Sus(vagueSaid) - 0.5) < 1e-9 && meSaid.Contains("\"result\":\"contradiction\"")
           && vague.EngineFor("sam").Answers.Count == 0, vagueSaid + " | " + meSaid);

        // A LIE FOUND OUT LATER (town list 6am): his answer, unjudged when given,
        // is caught once the game learns where this person saw him; and what he
        // told somebody else, reaching Sheila, is set against what she saw.
        var laterH = new Helper(new FakeLlm { Next = "Where were you on Tuesday night, then?" }, TimeSpan.FromSeconds(8));
        LoadCards(laterH, cardsDir);
        LoadCast(laterH, cardsDir);
        string noSight = "\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23},\"suspicion\":0.5,\"suspicionWhy\":\"I saw him near the window\"";
        string withSight = "\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23,\"sawHimAt\":\"ritas_counter\"},\"suspicion\":0.5,\"suspicionWhy\":\"I saw him near the window\"";
        await laterH.Answer("{\"id\":130,\"to\":\"sam\",\"say\":\"Evening.\",\"day\":2,\"hour\":10," + noSight + "}");
        string unjudged = await laterH.Answer("{\"id\":131,\"to\":\"sam\",\"say\":\"I was at the chapel all night.\",\"day\":2,\"hour\":10," + noSight + "}");
        string caught = await laterH.Answer("{\"id\":132,\"to\":\"sam\",\"say\":\"Nice weather.\",\"day\":2,\"hour\":18," + withSight + "}");
        string afterCaught = await laterH.Answer("{\"id\":133,\"to\":\"sam\",\"say\":\"Well?\",\"day\":2,\"hour\":18," + withSight + "}");
        string toldSheila = await laterH.Answer("{\"id\":134,\"to\":\"lena\",\"say\":\"Evening.\",\"day\":2,\"hour\":18,\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23,\"sawHimAt\":\"ritas_counter\",\"heardHeSaid\":\"chapel\"},\"suspicion\":0.5,\"suspicionWhy\":\"I saw him near the window\"}");
        string fishTold = await laterH.Answer("{\"id\":135,\"to\":\"rocco\",\"say\":\"Evening.\",\"day\":2,\"hour\":18,\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23,\"sawHimAt\":\"fish_front\",\"heardHeSaid\":[\"fish_dock\",\"fish_market\"]},\"suspicion\":0.5,\"suspicionWhy\":\"I saw him near the window\"}");
        var noEvidence = new Helper(new FakeLlm { Next = "Where were you on Tuesday night, then?" }, TimeSpan.FromSeconds(8));
        LoadCards(noEvidence, cardsDir);
        LoadCast(noEvidence, cardsDir);
        string bare = "\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23";
        await noEvidence.Answer("{\"id\":140,\"to\":\"sam\",\"say\":\"Evening.\",\"day\":2,\"hour\":10," + bare + "}}");
        string ne1 = await noEvidence.Answer("{\"id\":141,\"to\":\"sam\",\"say\":\"I was at the chapel all night.\",\"day\":2,\"hour\":10," + bare + ",\"heardHimAt\":\"ritas\"}}");
        string ne2 = await noEvidence.Answer("{\"id\":142,\"to\":\"sam\",\"say\":\"Well?\",\"day\":2,\"hour\":11," + bare + ",\"heardHimAt\":\"ritas\",\"sawHimAt\":\"ritas_counter\"}}");
        string ne3 = await noEvidence.Answer("{\"id\":143,\"to\":\"sam\",\"say\":\"Well?\",\"day\":2,\"hour\":11," + bare + ",\"heardHimAt\":\"ritas\",\"sawHimAt\":\"ritas_counter\"}}");
        Ok("what he told others fits when any of its areas fits; without the game's evidence each thing counts once: hearsay half a lie, then the caught lie in all",
           Math.Abs(Sus(fishTold) - 0.5) < 1e-9 && Math.Abs(Sus(ne1) - ConversationEngine.LieWeight / 2) < 1e-6
           && Math.Abs(Sus(ne2) - ConversationEngine.LieWeight) < 1e-6 && Math.Abs(Sus(ne3) - ConversationEngine.LieWeight) < 1e-6, fishTold + " | " + ne1 + " | " + ne2 + " | " + ne3);
        Ok("an answer unjudged when given is caught once they know where he was, once; what he told others is set against what they saw",
           unjudged.Contains("\"result\":\"unknown\"") && caught.Contains("\"later\":true") && caught.Contains("\"result\":\"contradiction\"")
           && Sus(caught) > 0.5 + 0.1 && Math.Abs(Sus(afterCaught) - Sus(caught)) < 1e-6 && !afterCaught.Contains("\"later\":true")
           && Sus(toldSheila) > 0.5 + 0.05 && laterH.EngineFor("lena").BuildSystemPrompt("x", new GameTime(2, 18, 5), "").Contains("You have heard he has been telling people he was at the chapel"),
           unjudged + " | " + caught + " | " + toldSheila);

        // OWNING UP, AND "KEEP IT TO YOURSELF" (town list 6al): Darren says yes to
        // anybody and his silence is fragile; Ron keeps it quiet for the owner;
        // nobody keeps a grave deed quiet; "it was me" is remembered as told by him.
        var quiet = new Helper(new FakeLlm { Next = "Right you are." }, TimeSpan.FromSeconds(8));
        LoadCards(quiet, cardsDir);
        LoadCast(quiet, cardsDir);
        string qDeed = "\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23}";
        string qSam = await quiet.Answer("{\"id\":120,\"to\":\"sam\",\"say\":\"Keep it to yourself, Darren.\",\"day\":2,\"hour\":10," + qDeed + "}");
        string qRon = await quiet.Answer("{\"id\":121,\"to\":\"rocco\",\"say\":\"Yeah, it was me. Keep it to yourself.\",\"day\":2,\"hour\":10," + qDeed + "}");
        string qGrave = await quiet.Answer("{\"id\":122,\"to\":\"lena\",\"say\":\"Don't tell anyone.\",\"day\":2,\"hour\":10,\"deed\":{\"topic\":\"player.killing_d1\",\"day\":1,\"hour\":23,\"grave\":true}}");
        string qNone = await quiet.Answer("{\"id\":123,\"to\":\"sam\",\"say\":\"Nice weather.\",\"day\":2,\"hour\":10," + qDeed + "}");
        string qNoDeed = await quiet.Answer("{\"id\":124,\"to\":\"lena\",\"say\":\"Keep it to yourself, Sheila.\",\"day\":2,\"hour\":11}");
        Ok("asked to keep it quiet, the Core decides and the game is told: Darren yes and fragile, Ron yes for the owner, nobody for a killing; owning up is kept",
           qSam.Contains("\"keepsQuiet\":{\"topic\":\"player.window_d1\",\"agreed\":true,\"fragile\":true}")
           && qRon.Contains("\"ownedUp\":\"player.window_d1\"") && qRon.Contains("\"agreed\":true,\"fragile\":false")
           && qGrave.Contains("\"agreed\":false") && qNone.Contains("\"keepsQuiet\":null") && qNone.Contains("\"ownedUp\":null")
           && qNoDeed.Contains("\"keepsQuiet\":null") && !quiet.EngineFor("lena").KeepsQuiet.ContainsKey("player.window_d1")
           && quiet.EngineFor("rocco").BuildSystemPrompt("x", new GameTime(2, 10, 5), "").Contains("He has owned up to it"), qSam + " | " + qRon + " | " + qGrave);

        // TELLING RON NO (town list 6bn), in two steps: a line that sounds like a
        // no gets Ron's own question back, no model called; only a plain yes to
        // it within the hour is the no, and nobody remembers the no until the
        // game answers it; without the ask nothing is read.
        var askLlm = new FakeLlm { Next = "Right you are, boss." };
        var asker = new Helper(askLlm, TimeSpan.FromSeconds(8));
        LoadCards(asker, cardsDir);
        int callsBefore = askLlm.Calls;
        string aNo = await asker.Answer("{\"id\":130,\"to\":\"rocco\",\"say\":\"Tell them no, Ron.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        bool noModelCalled = askLlm.Calls == callsBefore;
        string aYes = await asker.Answer("{\"id\":131,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":0,\"hour\":21,\"minute\":2,\"ask\":{\"tonight\":true}}");
        string toldNoLine = asker.EngineFor("rocco").Tonight;
        string aYesAgain = await asker.Answer("{\"id\":132,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":0,\"hour\":21,\"minute\":3,\"ask\":{\"tonight\":true}}");
        string aNoAsk = await asker.Answer("{\"id\":133,\"to\":\"rocco\",\"say\":\"Tell them no, Ron.\",\"day\":0,\"hour\":21}");
        string noAskLine = asker.EngineFor("rocco").Tonight;
        string aMaybe = await asker.Answer("{\"id\":134,\"to\":\"rocco\",\"say\":\"What if I said no?\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        string askedLine = asker.EngineFor("rocco").Tonight;
        // Asked, then something else: the question lapses.
        await asker.Answer("{\"id\":135,\"to\":\"rocco\",\"say\":\"The drivers want Sunday off. Tell them no.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        string aOther = await asker.Answer("{\"id\":136,\"to\":\"rocco\",\"say\":\"No, the drivers, not the envelope.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        string aLateYes = await asker.Answer("{\"id\":137,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        Ok("a line to Ron that sounds like a no gets his own plain question, no model called; his plain yes to it is the no, reported and tonight's line for the reply, remembered by nobody until the game answers it; a yes with no question before it, any other answer, or no ask tonight is nothing",
           aNo.Contains("\"reply\":\"" + Arrangement.AskPlainly.Substring(0, 20)) && aNo.Contains("\"deal\":\"ron-tell-them-no\"") && aNo.Contains("\"refusedAsk\":false") && aNo.Contains("\"generated\":false") && noModelCalled
           && aYes.Contains("\"refusedAsk\":true") && aYes.Contains("\"reply\":\"" + Arrangement.TookNo.Substring(0, 20)) && aYes.Contains("\"generated\":false")
           && toldNoLine == Arrangement.TonightToldNo && aYesAgain.Contains("\"refusedAsk\":false")
           && aNoAsk.Contains("\"refusedAsk\":false") && !aNoAsk.Contains("\"reply\":\"" + Arrangement.AskPlainly.Substring(0, 20)) && noAskLine == null
           && aMaybe.Contains("\"refusedAsk\":false") && askedLine == Arrangement.TonightAsked
           && aOther.Contains("\"refusedAsk\":false") && aLateYes.Contains("\"refusedAsk\":false")
           && !asker.EngineFor("rocco").Memory.Events.Exists(e => e.Text == Arrangement.HeardNo || e.Text.StartsWith("He told me no")), aNo + " | " + aYes + " | " + aOther);
        // ACROSS ONE IN THE MORNING (the independent review of 30 September, B4a):
        // Ron's question put at two to one, while the ask stood, and his "Yes." at
        // two past, after it lapsed, is still the no, reported with the question's
        // time, so the game answers that night as of then.
        var lateAsker = new Helper(new FakeLlm { Next = "Right you are, boss." }, TimeSpan.FromSeconds(8));
        LoadCards(lateAsker, cardsDir);
        await lateAsker.Answer("{\"id\":138,\"to\":\"rocco\",\"say\":\"Tell them no, Ron.\",\"day\":1,\"hour\":0,\"minute\":58,\"ask\":{\"tonight\":true}}");
        string aPastOne = await lateAsker.Answer("{\"id\":139,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":1,\"hour\":1,\"minute\":2}");
        Ok("his yes at two past one to Ron's question at two to one is the no, reported as of the question, so the game answers the night Ron asked",
           aPastOne.Contains("\"refusedAsk\":true") && aPastOne.Contains("\"refusedAt\":{\"day\":1,\"hour\":0,\"minute\":58}"), aPastOne);
        // Three game hours on is too late (the second independent check: at exactly three
        // hours a yes still ended that night's arrangement, backdated).
        var slowAsker = new Helper(new FakeLlm { Next = "Right you are, boss." }, TimeSpan.FromSeconds(8));
        LoadCards(slowAsker, cardsDir);
        await slowAsker.Answer("{\"id\":140,\"to\":\"rocco\",\"say\":\"Tell them no, Ron.\",\"day\":1,\"hour\":0,\"minute\":58,\"ask\":{\"tonight\":true}}");
        string aThreeHours = await slowAsker.Answer("{\"id\":141,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":1,\"hour\":3,\"minute\":58}");
        Ok("a yes three game hours after Ron's question is nothing", aThreeHours.Contains("\"refusedAsk\":false"), aThreeHours);
        // Walking away clears the question: back again, a yes is nothing.
        var walkAsker = new Helper(new FakeLlm { Next = "Right." }, TimeSpan.FromSeconds(8));
        LoadCards(walkAsker, cardsDir);
        await walkAsker.Answer("{\"id\":140,\"to\":\"rocco\",\"say\":\"Count me out.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        await walkAsker.Answer("{\"walkedAway\":{\"to\":\"rocco\",\"heard\":\"\"},\"day\":0,\"hour\":21}");
        string aBack = await walkAsker.Answer("{\"id\":141,\"to\":\"rocco\",\"say\":\"Yes mate.\",\"day\":0,\"hour\":21,\"minute\":20,\"ask\":{\"tonight\":true}}");
        await walkAsker.Answer("{\"id\":142,\"to\":\"rocco\",\"say\":\"No thanks.\",\"day\":0,\"hour\":21,\"minute\":30,\"ask\":{\"tonight\":true}}");
        string aPlease = await walkAsker.Answer("{\"id\":143,\"to\":\"rocco\",\"say\":\"Yes please\",\"day\":0,\"hour\":22,\"minute\":50,\"ask\":{\"tonight\":true}}");
        Ok("walking away clears Ron's question, so a yes on his return is nothing; \"No thanks.\" gets the question, and \"Yes please\" nearly three game hours later is the no",
           aBack.Contains("\"refusedAsk\":false") && aPlease.Contains("\"refusedAsk\":true"), aBack + " | " + aPlease);
        // Backing out of Ron's question, or a line to somebody else, is no yes;
        // and nobody but Ron is read for it.
        var backAsker = new Helper(new FakeLlm { Next = "Right." }, TimeSpan.FromSeconds(8));
        LoadCards(backAsker, cardsDir);
        await backAsker.Answer("{\"id\":150,\"to\":\"rocco\",\"say\":\"Tell them no, Ron.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        string aBackOut = await backAsker.Answer("{\"id\":151,\"to\":\"rocco\",\"say\":\"No thanks.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        await backAsker.Answer("{\"id\":152,\"to\":\"rocco\",\"say\":\"Count me out.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        await backAsker.Answer("{\"id\":153,\"to\":\"sam\",\"say\":\"Alright, Darren.\",\"day\":0,\"hour\":21}");
        string aAfterOther = await backAsker.Answer("{\"id\":154,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        string aToDarren = await backAsker.Answer("{\"id\":155,\"to\":\"sam\",\"say\":\"Tell them no.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        await backAsker.Answer("{\"id\":160,\"to\":\"rocco\",\"say\":\"Forget it.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        string aTellYes = await backAsker.Answer("{\"id\":156,\"to\":\"rocco\",\"say\":\"Tell them okay.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        await backAsker.Answer("{\"id\":157,\"to\":\"rocco\",\"say\":\"Forget it.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        await backAsker.Answer("{\"id\":158,\"to\":\"nobodyhere\",\"say\":\"Evening.\",\"day\":0,\"hour\":21}");
        string aAfterNobody = await backAsker.Answer("{\"id\":159,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":0,\"hour\":21,\"ask\":{\"tonight\":true}}");
        Ok("\"No thanks.\" said back to Ron's question ends nothing and does not bring it back; a line to anybody else, carded or not, clears the question; a line to anybody but Ron is never read for it",
           aBackOut.Contains("\"refusedAsk\":false") && !aBackOut.Contains("\"reply\":\"" + Arrangement.AskPlainly.Substring(0, 20))
           && aAfterOther.Contains("\"refusedAsk\":false") && aToDarren.Contains("\"refusedAsk\":false")
           && aTellYes.Contains("\"refusedAsk\":false") && aAfterNobody.Contains("\"refusedAsk\":false")
           && !aToDarren.Contains("\"reply\":\"" + Arrangement.AskPlainly.Substring(0, 20)), aBackOut + " | " + aAfterOther + " | " + aToDarren + " | " + aAfterNobody);
        // Asked more than three game hours ago, a yes is not his no.
        var staleAsker = new Helper(new FakeLlm { Next = "Right." }, TimeSpan.FromSeconds(8));
        LoadCards(staleAsker, cardsDir);
        await staleAsker.Answer("{\"id\":138,\"to\":\"rocco\",\"say\":\"I'm not doing it.\",\"day\":0,\"hour\":19,\"ask\":{\"tonight\":true}}");
        string aStale = await staleAsker.Answer("{\"id\":139,\"to\":\"rocco\",\"say\":\"Yes.\",\"day\":0,\"hour\":22,\"minute\":1,\"ask\":{\"tonight\":true}}");
        string staleLine = staleAsker.EngineFor("rocco").Tonight;
        Ok("a yes to Ron's question of more than three game hours ago is not read as his no", aStale.Contains("\"refusedAsk\":false") && staleLine == Arrangement.TonightAsked, aStale);

        // WALKING OFF STOPS THE REPLY AT ONCE (town list 6ay).
        var slowTalk = new FakeLlm { Next = "Well, the thing about the rank is this.", Delay = TimeSpan.FromSeconds(4) };
        var offWalker = new Helper(slowTalk, TimeSpan.FromSeconds(8));
        LoadCards(offWalker, cardsDir);
        var walkWatch = Stopwatch.StartNew();
        var pendingReply = offWalker.Answer("{\"id\":160,\"to\":\"rocco\",\"say\":\"What's the rank like?\",\"day\":2,\"hour\":18}");
        await Task.Delay(300);
        string walkLine = "{\"walkedAway\":{\"to\":\"rocco\",\"heard\":\"\"},\"day\":2,\"hour\":18}";
        bool stopped = offWalker.WalkOffIfFor(walkLine);
        string stoppedReply = await pendingReply;
        long stoppedMs = walkWatch.ElapsedMilliseconds;
        string noted = await offWalker.Answer(walkLine);
        var offEngine = offWalker.EngineFor("rocco");
        int leftNotes = offEngine.Memory.Events.FindAll(ev => ev.Text == "He walked off while I was still talking to him.").Count;
        Ok("walking off stops the reply being written at once; they remember his line, that they said nothing he heard, and that he left, once",
           stopped && stoppedReply.Contains("\"walkedOff\":true") && stoppedMs < 2500 && noted.Contains("\"noted\":true") && leftNotes == 1
           && offEngine.Memory.Events.Exists(ev => ev.Text.Contains("What's the rank like?")) && offEngine.Memory.Events.Exists(ev => ev.Text.Contains("he walked off before I could answer"))
           && !offWalker.WalkOffIfFor(walkLine), stoppedReply + " | " + noted + " | " + stoppedMs);

        // TALK THAT CANNOT BE REACHED (town list 6ax): the brush-off, and the player told.
        var broken = new Helper(new BrokenFake(), TimeSpan.FromSeconds(8));
        LoadCards(broken, cardsDir);
        string brokenLine = await broken.Answer("{\"id\":150,\"to\":\"rocco\",\"say\":\"Evening.\",\"day\":2,\"hour\":18}");
        var noModel = new Helper(null, TimeSpan.FromSeconds(8));
        LoadCards(noModel, cardsDir);
        string offLine = await noModel.Answer("{\"id\":151,\"to\":\"lena\",\"say\":\"Morning.\",\"day\":2,\"hour\":9}");
        Ok("talk that cannot be reached, or is off in this copy, says so plainly beside the brush-off",
           Str(brokenLine, "paused") == AiNotice.TalkUnreachable && broken.Cards["rocco"].OwnWords["brush-off"].Contains(Reply(brokenLine))
           && Str(offLine, "paused") == AiNotice.TalkOff && Flag(offLine, "offline"), brokenLine + " | " + offLine);

        // THE REHEARSAL (town list 6aw): a session end to end, every kind of line
        // the protocol page names, in the order a friend's half hour would bring
        // them; every answer parses, and says nothing the page does not name.
        {
            var specPath = Path.Combine(cardsDir, "..", "..", "specs", "talk-protocol.md");
            var named = new HashSet<string>();
            foreach (System.Text.RegularExpressions.Match m in System.Text.RegularExpressions.Regex.Matches(File.ReadAllText(specPath), "[`\"]([A-Za-z]+)[`\"]")) named.Add(m.Groups[1].Value);
            var talkModel = new ScriptFake(
                "Morning. You'll be the new owner.",
                "That's Ron. He keeps the rank.",
                "Where were you on Tuesday night?",
                "Were you now.",
                "Well. We'll see.",
                "Evening.",
                "Evening, then.");
            var rehearse = new Helper(talkModel, TimeSpan.FromSeconds(8));
            LoadCards(rehearse, cardsDir);
            LoadCast(rehearse, cardsDir);
            var outs = new List<string>();
            async Task<string> Say(string line) { var o = await rehearse.Answer(line); outs.Add(o); return o; }
            string deed = "\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23,\"sawHimAt\":\"ritas_counter\"}";
            string evidence = "\"evidence\":{\"account\":{\"held\":true,\"seen\":true,\"names\":false,\"rung\":2,\"confidence\":0.8,\"summary\":\"somebody at Rita's window\"},\"near\":{\"sawHim\":true,\"heard\":false,\"others\":1,\"summary\":\"he was about\"},\"familiarity\":0.3}";
            string savePath = Path.Combine(Path.GetTempPath(), "ledger-rehearsal-" + Guid.NewGuid().ToString("N") + ".talk.json");
            await Say("{\"talk\":\"reset\"}");
            await Say("{\"id\":200,\"to\":\"sam\",\"who\":\"sam\",\"say\":\"Morning.\",\"day\":2,\"hour\":9,\"minute\":5,\"scene\":\"Dry, grey.\",\"fresh\":true,\"acquaintance\":{\"met\":false,\"heardOf\":true},\"present\":[\"rocco\"]}");
            await Say("{\"id\":201,\"to\":\"sam\",\"say\":\"Who's that at the rank?\",\"day\":2,\"hour\":9,\"minute\":6,\"present\":[\"rocco\"],\"knowing\":{\"level\":\"little\",\"story\":\"player.window_d1\"}}");
            await Say("{\"id\":202,\"to\":\"lena\",\"say\":\"Morning, Sheila.\",\"day\":2,\"hour\":10,\"minute\":0,\"fresh\":true," + evidence + "," + deed + ",\"memories\":[{\"day\":1,\"hour\":23,\"minute\":5,\"kind\":\"observation\",\"importance\":0.8,\"text\":\"Somebody put Rita's window in.\",\"story\":\"player.window_d1\"}]}");
            string rLie = await Say("{\"id\":203,\"to\":\"lena\",\"say\":\"I was at the chapel all night.\",\"day\":2,\"hour\":10,\"minute\":1," + evidence + "," + deed + "}");
            string owned = await Say("{\"id\":204,\"to\":\"lena\",\"say\":\"All right, it was me. Keep it to yourself.\",\"day\":2,\"hour\":10,\"minute\":2," + evidence + "," + deed + "}");
            string level = await Say("{\"id\":205,\"to\":\"rocco\",\"noReply\":true,\"day\":2,\"hour\":11," + evidence + "}");
            await Say("{\"id\":206,\"to\":\"rocco\",\"say\":\"Evening.\",\"day\":2,\"hour\":18}");
            await Say("{\"walkedAway\":{\"to\":\"rocco\",\"heard\":\"Evening\"},\"day\":2,\"hour\":18}");
            string reported = await Say("{\"report\":203,\"why\":\"a test of the button\"}");
            string saved = await Say("{\"talk\":\"save\",\"path\":" + JsonSerializer.Serialize(savePath) + ",\"stamp\":\"rehearsal\"}");
            string loaded = await Say("{\"talk\":\"load\",\"path\":" + JsonSerializer.Serialize(savePath) + ",\"stamp\":\"rehearsal\"}");
            bool keptLie = rehearse.EngineFor("lena") != null && rehearse.EngineFor("lena").OwnedUp.Contains("player.window_d1") && rehearse.EngineFor("lena").Answers.Count == 1;
            await Say("{\"id\":207,\"to\":\"lena\",\"say\":\"Still here.\",\"day\":2,\"hour\":12}");
            string reset = await Say("{\"talk\":\"reset\"}");
            try { File.Delete(savePath); } catch (IOException) { }
            string stray = null;
            void Keys(JsonElement e)
            {
                if (e.ValueKind != JsonValueKind.Object) return;
                foreach (var p in e.EnumerateObject())
                {
                    if (!named.Contains(p.Name)) stray = p.Name;
                    if (p.Value.ValueKind == JsonValueKind.Object) Keys(p.Value);
                }
            }
            bool allParse = true;
            foreach (var o in outs)
            {
                try { using var rd = JsonDocument.Parse(o); Keys(rd.RootElement); }
                catch (JsonException) { allParse = false; }
            }
            Ok("a rehearsed session: every kind of line answered, every answer parses and names only what the protocol page names; the lie, the owning up and the silence survive a save and a load",
               allParse && stray == null && outs.Count == 14 && rLie.Contains("\"result\":\"contradiction\"") && owned.Contains("\"ownedUp\":\"player.window_d1\"")
               && owned.Contains("\"agreed\":true") && level.Contains("\"level\"") && !level.Contains("\"reply\"") && reported.Contains("\"found\":true")
               && saved.Contains("\"talk\":\"saved\"") && loaded.Contains("\"talk\":\"loaded\"") && keptLie && reset.Contains("\"talk\":\"reset\""),
               (stray ?? "") + " | " + rLie + " | " + owned + " | " + saved + " | " + loaded);
        }

        // WHERE THEY ARE (town list 6u): each person told their own place this hour.
        var placed = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
        LoadCards(placed, cardsDir);
        LoadCast(placed, cardsDir);
        int placedDay = -1, placedHour = -1; string placedWords = null;
        for (int dd = 0; dd < 7 && placedWords == null; dd++)
            for (int hh = 8; hh < 20 && placedWords == null; hh++)
                if (placed.Cast?.WhereWords("sam", dd, hh) is string ww) { placedDay = dd; placedHour = hh; placedWords = ww; }
        await placed.Answer("{\"id\":81,\"to\":\"sam\",\"say\":\"Morning.\",\"day\":" + placedDay + ",\"hour\":" + placedHour + ",\"scene\":\"Quay Street, by the parade.\"}");
        string placedPrompt = placed.EngineFor("sam") == null ? "" : placed.EngineFor("sam").BuildSystemPrompt("Morning.", new GameTime(placedDay, placedHour, 0), "");
        Ok("the cast's routines are read, and a person is told where they are this hour beside the game's scene",
           placed.Cast != null && placedWords != null && placed.LastScene == "Quay Street, by the parade. Where you are: " + placedWords + ".", placed.LastScene ?? "no scene");
        Ok("and who they know on the street, where their friends usually are, and the street's places (town list 6ad)",
           placedPrompt.Contains("- Ron Kirby, who keeps Mickey's door and the rank; you know each other well; usually at Mickey's most of the day.")
           && placedPrompt.Contains("; everybody on the street knows who that is.") && placedPrompt.Contains("The street's places, as people call them: "), placedPrompt);
        await placed.Answer("{\"id\":82,\"to\":\"sam\",\"say\":\"Who's that?\",\"day\":" + placedDay + ",\"hour\":" + placedHour + ",\"present\":[\"rita\",\"nobody\"]}");
        string presentPrompt = placed.EngineFor("sam").BuildSystemPrompt("Who's that?", new GameTime(placedDay, placedHour, 0), "");
        Ok("who the game says is with them is who they see", presentPrompt.Contains("- Here with you now: Rita.") , presentPrompt);

        // THE RELAY SAYS NO (town list 6t): a brush-off, and the player told why.
        var refused = new Helper(new RefusingFake(), TimeSpan.FromSeconds(8));
        LoadCards(refused, cardsDir);
        string spentLine = await refused.Answer("{\"id\":71,\"to\":\"sam\",\"say\":\"Morning.\"}");
        Ok("when the allowance is spent the character brushes him off and the player is told why and when",
           Str(spentLine, "paused") == AiNotice.TalkPaused("allowance_spent", "tomorrow") && Str(spentLine, "paused").Contains("tomorrow")
           && !Flag(spentLine, "timedOut") && Reply(spentLine) != null, spentLine);

        // HOW THEY KNOW HIM (town list 6s): the game's acquaintance reaches the prompt.
        var knower = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
        LoadCards(knower, cardsDir);
        await knower.Answer("{\"id\":60,\"to\":\"lena\",\"say\":\"Morning.\"}");
        string firstTime = knower.EngineFor("lena").HowYouKnowHim;
        await knower.Answer("{\"id\":63,\"to\":\"lena\",\"say\":\"Me again.\"}");
        Ok("with nothing from the game, a first talk is a first meeting; the next, they have spoken before, and nobody has told them his name",
           firstTime.Contains("for the first time") && knower.EngineFor("lena").HowYouKnowHim.Contains("You have spoken with")
           && knower.EngineFor("lena").HowYouKnowHim.Contains("you call him the new owner"), knower.EngineFor("lena").HowYouKnowHim);
        await knower.Answer("{\"id\":64,\"to\":\"lena\",\"say\":\"Still me.\",\"acquaintance\":{\"met\":false}}");
        Ok("the game cannot make them forget a talk they have had", !knower.EngineFor("lena").HowYouKnowHim.Contains("for the first time"), knower.EngineFor("lena").HowYouKnowHim);
        await knower.Answer("{\"id\":61,\"to\":\"sam\",\"say\":\"Morning.\",\"acquaintance\":{\"met\":true,\"calls\":\"Tom\"}}");
        string knowPrompt = knower.EngineFor("sam").BuildSystemPrompt("Morning.", new GameTime(1, 12, 0), "");
        await knower.Answer("{\"id\":62,\"to\":\"sam\",\"say\":\"Still here.\"}");
        Ok("what the game says a person calls Tom reaches their talk, and holds until it says otherwise",
           knowPrompt.Contains("you call him Tom") && knower.EngineFor("sam").HowYouKnowHim.Contains("you call him Tom") && !knowPrompt.Contains("I have never met"), knowPrompt.Length.ToString());
        // Sheila names him only once she trusts him (Jafar, 29 September page).
        var trusting = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
        LoadCards(trusting, cardsDir);
        LoadCast(trusting, cardsDir);
        await trusting.Answer("{\"id\":65,\"to\":\"lena\",\"say\":\"Morning.\",\"acquaintance\":{\"met\":true,\"calls\":\"Nowak\"}}");
        string untrusted = trusting.EngineFor("lena").HowYouKnowHim;
        await trusting.Answer("{\"id\":66,\"to\":\"sam\",\"say\":\"Morning.\",\"acquaintance\":{\"met\":true,\"calls\":\"Nowak\"}}");
        await trusting.Answer("{\"id\":67,\"to\":\"lena\",\"say\":\"Morning.\",\"acquaintance\":{\"met\":true,\"calls\":\"Nowak\",\"trusts\":true}}");
        string trusted = trusting.EngineFor("lena").HowYouKnowHim;
        await trusting.Answer("{\"id\":68,\"to\":\"lena\",\"say\":\"Still me.\",\"acquaintance\":{\"met\":true,\"calls\":\"Nowak\"}}");
        string stillTrusted = trusting.EngineFor("lena").HowYouKnowHim;
        await trusting.Answer("{\"id\":69,\"to\":\"lena\",\"say\":\"And again.\",\"acquaintance\":{\"met\":true,\"calls\":\"Nowak\",\"trusts\":false}}");
        Ok("Sheila calls him the new owner whatever name the game sends, until it says she trusts him, and that holds until it says otherwise; Darren takes the name at once",
           untrusted.Contains("you call him the new owner") && trusting.EngineFor("sam").HowYouKnowHim.Contains("you call him Nowak")
           && trusted.Contains("you call him Nowak") && stillTrusted.Contains("you call him Nowak")
           && trusting.EngineFor("lena").HowYouKnowHim.Contains("you call him the new owner"), untrusted);
        await trusting.Answer("{\"id\":70,\"to\":\"lena\",\"who\":\"zlata\",\"say\":\"Morning.\"}");
        // SHE COMES TO TRUST HIM (town list 6bz): talk with her on three different
        // days and the reply says so, once for the timeline; the game's "false"
        // never undoes it; it survives a load; with talk off it still comes.
        {
            string TalkTo(Helper h, int n, string who, int d, string say = "Morning.", string extra = "") =>
                h.Answer("{\"id\":" + n + ",\"to\":\"" + who + "\",\"day\":" + d + ",\"hour\":11,\"say\":" + JsonSerializer.Serialize(say) + ",\"acquaintance\":{\"met\":true,\"calls\":\"Nowak\"" + extra + "}}").Result;
            Helper Fresh(ILlmClient llm)
            {
                var h = new Helper(llm, TimeSpan.FromSeconds(8));
                LoadCards(h, cardsDir);
                LoadCast(h, cardsDir);
                return h;
            }
            var earns = Fresh(new FakeLlm());
            string d0 = TalkTo(earns, 71, "lena", 0), d1 = TalkTo(earns, 72, "lena", 1), d2 = TalkTo(earns, 73, "lena", 2);
            string nextTurn = TalkTo(earns, 74, "lena", 2);
            string namesHim = earns.EngineFor("lena").HowYouKnowHim;
            string darren = TalkTo(earns, 75, "sam", 2);
            string gameSaysNo = TalkTo(earns, 76, "lena", 3, extra: ",\"trusts\":false");
            // Kept with the talk: after a load, no second "earned", and her name at once.
            string trustDir = Path.Combine(Path.GetTempPath(), "talkhelper-trust-" + Guid.NewGuid().ToString("N"));
            Directory.CreateDirectory(trustDir);
            string afterLoad, loadNames;
            try
            {
                string slot = Path.Combine(trustDir, "slot.talk.json");
                await earns.Answer("{\"talk\":\"save\",\"path\":" + JsonSerializer.Serialize(slot) + "}");
                await earns.Answer("{\"talk\":\"load\",\"path\":" + JsonSerializer.Serialize(slot) + "}");
                afterLoad = TalkTo(earns, 77, "lena", 3);
                loadNames = earns.EngineFor("lena").HowYouKnowHim;
            }
            finally { try { Directory.Delete(trustDir, true); } catch (Exception) { } }
            await earns.Answer("{\"talk\":\"reset\"}");
            string afterReset = TalkTo(earns, 78, "lena", 3);
            // A game that keeps a plain false from the start still hears it earned.
            var keptFalse = Fresh(new FakeLlm());
            TalkTo(keptFalse, 81, "lena", 0, extra: ",\"trusts\":false"); TalkTo(keptFalse, 82, "lena", 1, extra: ",\"trusts\":false");
            string falseEarned = TalkTo(keptFalse, 83, "lena", 2, extra: ",\"trusts\":false");
            // An empty line is no day he talked.
            var silent = Fresh(new FakeLlm());
            TalkTo(silent, 84, "lena", 0, ""); TalkTo(silent, 85, "lena", 1, "  ");
            string silentDay = TalkTo(silent, 86, "lena", 2);
            // With live talk off, the days still count, and the offline reply says so.
            var talkOff = Fresh(null);
            TalkTo(talkOff, 87, "lena", 0); TalkTo(talkOff, 88, "lena", 1);
            string offEarned = TalkTo(talkOff, 89, "lena", 2);
            // She saw him by Rita's the night of the window, and he never gave her
            // a plain answer her eyes bore out: no trust (the independent check).
            var sawHim = Fresh(new FakeLlm());
            TalkTo(sawHim, 90, "lena", 2, extra: "}, \"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23,\"sawHimAt\":\"ritas_counter\"");
            TalkTo(sawHim, 91, "lena", 3);
            string sawNoTrust = TalkTo(sawHim, 92, "lena", 4);
            // Trust the game granted first is never announced again.
            var granted = Fresh(new FakeLlm());
            string grantedFirst = TalkTo(granted, 93, "lena", 0, extra: ",\"trusts\":true");
            TalkTo(granted, 94, "lena", 1);
            string grantedThird = TalkTo(granted, 95, "lena", 2);
            // Her third day of talk is the day she puts her question over the
            // day-book: not earned that day; the day after, it is.
            var weekDay = Fresh(new FakeLlm());
            TalkTo(weekDay, 96, "lena", 0); TalkTo(weekDay, 97, "lena", 3);
            string weekTurn = weekDay.Answer("{\"id\":98,\"to\":\"lena\",\"day\":6,\"hour\":10,\"say\":\"Morning.\",\"week\":{\"ask\":true,\"realBook\":false,\"dayOff\":true}}").Result;
            string weekLater = weekDay.Answer("{\"id\":99,\"to\":\"lena\",\"day\":6,\"hour\":11,\"say\":\"How are the books?\",\"week\":{\"stands\":true,\"realBook\":false}}").Result;
            // Answered, and a line later that day without the question: still not that day.
            weekDay.Answer("{\"id\":116,\"to\":\"lena\",\"day\":6,\"hour\":11,\"say\":\"None of your business.\",\"week\":{\"stands\":true,\"realBook\":false}}").Wait();
            string answered = weekDay.Answer("{\"id\":117,\"to\":\"lena\",\"day\":6,\"hour\":11,\"say\":\"Yes.\",\"week\":{\"stands\":true,\"realBook\":false}}").Result;
            string laterThatDay = weekDay.Answer("{\"id\":118,\"to\":\"lena\",\"day\":6,\"hour\":12,\"say\":\"So can I see the other book now?\"}").Result;
            string dayAfter = TalkTo(weekDay, 100, "lena", 7);
            // Seen near a deed with no place named: still a sighting.
            var nearOnly = Fresh(new FakeLlm());
            string nearEvidence = "\"evidence\":{\"near\":{\"sawHim\":true,\"others\":0,\"summary\":\"he was about\"},\"familiarity\":0.2}";
            for (int nd = 1; nd <= 3; nd++) nearOnly.Answer("{\"id\":" + (111 + nd) + ",\"to\":\"lena\",\"day\":" + nd + ",\"hour\":11,\"say\":\"Morning.\"," + nearEvidence + "}").Wait();
            string nearFourth = TalkTo(nearOnly, 115, "lena", 4);
            Ok("trust is not earned while her week's question stands, and comes the day after; a sighting near a deed with no place named keeps it back too",
               weekTurn.Contains("\"trustEarned\":false") && weekLater.Contains("\"trustEarned\":false") && answered.Contains("\"weekAnswer\":\"WontSay\"")
               && laterThatDay.Contains("\"trustEarned\":false") && dayAfter.Contains("\"trusts\":true,\"trustEarned\":true")
               && nearFourth.Contains("\"trusts\":false"), weekTurn + " | " + dayAfter + " | " + nearFourth);
            Ok("a sighting of him at a deed with no plain answer her eyes bore out keeps her trust back; trust the game granted is never announced a second time",
               sawNoTrust.Contains("\"trusts\":false,\"trustEarned\":false") && grantedFirst.Contains("\"trusts\":true")
               && grantedThird.Contains("\"trusts\":true,\"trustEarned\":false"), sawNoTrust + " | " + grantedThird);
            Ok("Sheila comes to trust him on the third day he talks with her, said once for the timeline, a load keeping it and her name at once; the game's false never undoes it, and one kept from the start still hears it; nobody else carries it; an empty line is no day; with talk off it still comes; a reset forgets it",
               d0.Contains("\"trusts\":false") && d1.Contains("\"trusts\":false,\"trustEarned\":false")
               && d2.Contains("\"trusts\":true,\"trustEarned\":true") && nextTurn.Contains("\"trusts\":true,\"trustEarned\":false")
               && namesHim.Contains("you call him Nowak") && darren.Contains("\"trusts\":null")
               && gameSaysNo.Contains("\"trusts\":true,\"trustEarned\":false")
               && afterLoad.Contains("\"trusts\":true,\"trustEarned\":false") && loadNames.Contains("you call him Nowak")
               && afterReset.Contains("\"trusts\":false")
               && falseEarned.Contains("\"trusts\":true,\"trustEarned\":true")
               && silentDay.Contains("\"trusts\":false,\"trustEarned\":false")
               && offEarned.Contains("\"offline\":true") && offEarned.Contains("\"trusts\":true,\"trustEarned\":true"),
               d2 + " | " + afterLoad + " | " + loadNames + " | " + offEarned);
        }
        // THE WEEK'S END (town list 6ca): her question in her own fixed words, her
        // plain question to a line that sounds like one answer, his yes to it
        // as his very next line to her is his answer; with talk off too.
        {
            string Line(Helper h, int n, string who, string say, string week) =>
                h.Answer("{\"id\":" + n + ",\"to\":\"" + who + "\",\"day\":6,\"hour\":10,\"say\":" + JsonSerializer.Serialize(say) + (week == null ? "" : ",\"week\":" + week) + "}").Result;
            Helper WeekHelper(ILlmClient llm)
            {
                var h = new Helper(llm, TimeSpan.FromSeconds(8));
                LoadCards(h, cardsDir);
                LoadCast(h, cardsDir);
                return h;
            }
            const string Ask = "{\"ask\":true,\"realBook\":true,\"dayOff\":true}", Stands = "{\"stands\":true,\"realBook\":true}";
            Helper WeekHelperAsked()
            {
                var h = WeekHelper(null);
                Line(h, 119, "lena", "I'm taking it over.", Stands);
                return h;
            }
            var wh = WeekHelper(new FakeLlm());
            string opened = Line(wh, 101, "lena", "Morning, Sheila.", Ask);
            string sounds = Line(wh, 102, "lena", "I'm taking it over.", Stands);
            string yes = Line(wh, 103, "lena", "Yes.", Stands);
            // Mixed, or not asked: no plain question; a line to somebody else between clears it.
            string mixed = Line(wh, 104, "lena", "Take it over or wind it down, I can't tell.", Stands);
            string noWeek = Line(wh, 105, "lena", "I'm taking it over.", null);
            string windDown = Line(wh, 106, "lena", "I'm winding it down.", Stands);
            Line(wh, 107, "sam", "Morning.", null);
            string lateYes = Line(wh, 108, "lena", "Yes.", Stands);
            string toSam = Line(wh, 109, "sam", "I'm taking it over.", Stands);
            // With talk off: the fixed lines still come.
            var weekOff = WeekHelper(null);
            string offSounds = Line(weekOff, 110, "lena", "Wind it down.", Stands);
            string offYes = Line(weekOff, 111, "lena", "Yes, that's my answer.", Stands);
            // A clear answer while her plain question waits for another gets the
            // plain question for this one, and his yes to it is his answer.
            var changes = WeekHelper(null);
            Line(changes, 120, "lena", "Wind it down.", Stands);
            string otherAnswer = Line(changes, 121, "lena", "I'm taking it over.", Stands);
            string changedYes = Line(changes, 122, "lena", "Yes.", Stands);
            string shrug = Line(WeekHelperAsked(), 123, "lena", "Yeah, yeah.", Stands);
            // Mickey's arrangement already ended: her plain question never offers it (town list 6cc).
            string endedAsk = Line(WeekHelper(null), 124, "lena", "I'm taking it over.", "{\"stands\":true,\"realBook\":true,\"ended\":true}");
            var weekOff2 = WeekHelper(null);
            string offWhat = Line(weekOff2, 112, "lena", "What do you mean?", Stands);
            Ok("the week's end: Sheila's question and her plain question in her own fixed words, his yes to it as his next line to her is his answer; a mixed line, a line without the question, a yes after a line to somebody else, or the question sent to somebody else is nothing; with talk off it all still comes",
               Reply(opened) == WeeksEnd.Opening(true, true) && opened.Contains("\"generated\":false")
               && Reply(sounds) == WeeksEnd.AskPlainly(WeekAnswer.TakeOver) && sounds.Contains("\"weekAnswer\":null") && sounds.Contains("\"deal\":\"sheila-week-takeover\"")
               && Reply(yes) == WeeksEnd.Took(WeekAnswer.TakeOver) && yes.Contains("\"weekAnswer\":\"TakeOver\"")
               && Reply(mixed) != WeeksEnd.AskPlainly(WeekAnswer.TakeOver) && !mixed.Contains("\"weekAnswer\":\"")
               && Reply(noWeek) != WeeksEnd.AskPlainly(WeekAnswer.TakeOver)
               && Reply(windDown) == WeeksEnd.AskPlainly(WeekAnswer.WindDown) && !lateYes.Contains("\"weekAnswer\":\"") && Reply(lateYes) != WeeksEnd.Took(WeekAnswer.WindDown)
               && Reply(toSam) != WeeksEnd.AskPlainly(WeekAnswer.TakeOver)
               && Reply(offSounds) == WeeksEnd.AskPlainly(WeekAnswer.WindDown) && Reply(offYes) == WeeksEnd.Took(WeekAnswer.WindDown)
               && offYes.Contains("\"weekAnswer\":\"WindDown\"") && offYes.Contains("\"offline\":true") && Reply(offWhat) == WeeksEnd.StillAsks
               && Reply(otherAnswer) == WeeksEnd.AskPlainly(WeekAnswer.TakeOver) && Reply(changedYes) == WeeksEnd.Took(WeekAnswer.TakeOver)
               && changedYes.Contains("\"weekAnswer\":\"TakeOver\"") && !shrug.Contains("\"weekAnswer\":\"")
               && Reply(endedAsk) == WeeksEnd.AskPlainly(WeekAnswer.TakeOver, true),
               opened + " | " + sounds + " | " + yes + " | " + offYes);
        }
        // WHAT THE STREET KNOWS (town list ck): every card has the street's plain
        // facts, the person a fact is about in their own words, never his name.
        {
            var sh = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
            LoadCards(sh, cardsDir);
            bool has(string who, string part) => sh.Cards.TryGetValue(who, out var c) && c.HardFacts.Exists(f => f.Contains(part));
            var all = new List<string>();
            foreach (var (_, _, fact, own, _, _) in StreetFacts.All) { all.Add(fact); if (own != null) all.Add(own); }
            var bad = all.FindAll(f => f.Contains("Tom") || f.Contains("Nowak") || ContentRule.SpeechBreaks(f) != null || SafetyRule.SpeechBreaks(f) != null);
            Ok("every talking character knows the street's plain facts (the door, the funeral, the will, the flat, the drivers, the hours, the trade, the cafe), the person a fact is about in their own words; none names him, and each passes the content rules",
               has("rocco", "The cafe is across the street")
               && has("sam", "Father Walsh's chapel") && has("lena", "and I keep the key") && !has("lena", "Sheila keeps the key") && has("rocco", "Sheila keeps the key")
               && bad.Count == 0,
               string.Join(" | ", bad));
        }

        // WHAT THEY CALL HIM, BY KNOWING (town list 6ch): the new owner until they
        // know his name, Nowak once he gives it, Tom from the second day; Mickey's
        // own know it from the start; Sheila only on trust; the game's name wins.
        {
            var nh = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
            LoadCards(nh, cardsDir);
            LoadCast(nh, cardsDir);
            // Ada and June have no card of their own here: they borrow Darren's.
            string Say(int n, string who, int d, string say, string extra = "") =>
                nh.Answer("{\"id\":" + n + ",\"to\":\"" + (who == "ada" || who == "june" ? "sam\",\"who\":\"" + who : who) + "\",\"day\":" + d + ",\"hour\":11,\"say\":" + JsonSerializer.Serialize(say) + ",\"acquaintance\":{\"met\":true" + extra + "}}").Result;
            string adaFirst = Say(141, "ada", 0, "Morning.");
            string adaTold = Say(142, "ada", 0, "I'm Tom Nowak, Mickey's nephew.");
            string adaNext = Say(143, "ada", 1, "Morning, Ada.");
            string darren = Say(144, "sam", 0, "Morning.");
            string darrenAsked = Say(145, "sam", 0, "Call me Tom.");
            string sheila = Say(146, "lena", 3, "Morning.");
            string gameSays = Say(147, "june", 0, "Morning.", ",\"calls\":\"Tom\"");
            // Asked, not earned: no friend's silence on a first meeting (the independent check).
            string deedLine = ",\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23}";
            var fh = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
            LoadCards(fh, cardsDir);
            LoadCast(fh, cardsDir);
            fh.Answer("{\"id\":148,\"to\":\"sam\",\"who\":\"noor\",\"day\":0,\"hour\":11,\"say\":\"Call me Tom.\",\"acquaintance\":{\"met\":true}" + deedLine + "}").Wait();
            // Days before she knew his name do not count (the second review).
            fh.Answer("{\"id\":150,\"to\":\"sam\",\"who\":\"rita\",\"day\":0,\"hour\":11,\"say\":\"Morning.\",\"acquaintance\":{\"met\":true}}").Wait();
            fh.Answer("{\"id\":151,\"to\":\"sam\",\"who\":\"rita\",\"day\":1,\"hour\":11,\"say\":\"Morning.\",\"acquaintance\":{\"met\":true}}").Wait();
            string toldLate = fh.Answer("{\"id\":152,\"to\":\"sam\",\"who\":\"rita\",\"day\":2,\"hour\":11,\"say\":\"I'm Tom Nowak.\",\"acquaintance\":{\"met\":true}}").Result;
            string nextDay = fh.Answer("{\"id\":153,\"to\":\"sam\",\"who\":\"rita\",\"day\":3,\"hour\":11,\"say\":\"Morning.\",\"acquaintance\":{\"met\":true}}").Result;
            // Mickey's own reach Tom on the second day (the third review), and a
            // name the game sends is kept on the next line without one.
            string darrenD1 = fh.Answer("{\"id\":154,\"to\":\"sam\",\"day\":0,\"hour\":11,\"say\":\"Morning.\",\"acquaintance\":{\"met\":true}}").Result;
            string darrenD2 = fh.Answer("{\"id\":155,\"to\":\"sam\",\"day\":1,\"hour\":11,\"say\":\"Morning.\",\"acquaintance\":{\"met\":true}}").Result;
            fh.Answer("{\"id\":156,\"to\":\"sam\",\"who\":\"june\",\"day\":0,\"hour\":12,\"say\":\"Morning.\",\"acquaintance\":{\"met\":true,\"calls\":\"Tom\"}}").Wait();
            string juneAfter = fh.Answer("{\"id\":157,\"to\":\"sam\",\"who\":\"june\",\"day\":0,\"hour\":13,\"say\":\"Afternoon.\",\"acquaintance\":{\"met\":true}}").Result;
            string askedOnly = fh.Answer("{\"id\":149,\"to\":\"sam\",\"who\":\"noor\",\"day\":0,\"hour\":11,\"say\":\"Keep it to yourself.\",\"acquaintance\":{\"met\":true}" + deedLine + "}").Result;
            Ok("what they call him goes by knowing when the game sends no name: the new owner, Nowak once told, Tom the next day; Darren knows it from Mickey and takes Tom when asked; Sheila only on trust; the game's own name wins",
               adaFirst.Contains("\"calls\":\"the new owner\"") && adaTold.Contains("\"calls\":\"Nowak\"") && adaTold.Contains("\"gaveName\":true")
               && adaNext.Contains("\"calls\":\"Tom\"") && darren.Contains("\"calls\":\"Nowak\"") && darrenAsked.Contains("\"calls\":\"Tom\"")
               && sheila.Contains("\"calls\":\"the new owner\"") && gameSays.Contains("\"calls\":\"Tom\"")
               && !askedOnly.Contains("\"agreed\":true") && toldLate.Contains("\"calls\":\"Nowak\"") && nextDay.Contains("\"calls\":\"Tom\"")
               && darrenD1.Contains("\"calls\":\"Nowak\"") && darrenD2.Contains("\"calls\":\"Tom\"") && juneAfter.Contains("\"calls\":\"Tom\""),
               string.Join(" | ", Array.ConvertAll(new[] { adaFirst, adaTold, adaNext, darren, darrenAsked, sheila, gameSays, askedOnly, toldLate, nextDay, darrenD1, darrenD2, juneAfter }, r => System.Text.RegularExpressions.Regex.Match(r, "\"calls\":\"[^\"]*\"").Value)));
        }

        // A THREAT TO KEEP QUIET (town list 6cd): reported once a deed, never an ask for silence.
        {
            var th = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
            LoadCards(th, cardsDir);
            LoadCast(th, cardsDir);
            string deed = ",\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23}";
            string threatOnce = th.Answer("{\"id\":131,\"to\":\"sam\",\"day\":2,\"hour\":10,\"say\":\"Say a word and you'll regret it.\"" + deed + "}").Result;
            string threatAgain = th.Answer("{\"id\":132,\"to\":\"sam\",\"day\":2,\"hour\":10,\"say\":\"I know where you live.\"" + deed + "}").Result;
            string noDeed = th.Answer("{\"id\":133,\"to\":\"lena\",\"day\":2,\"hour\":10,\"say\":\"Say a word and you'll regret it.\"}").Result;
            // An ask after the threat, over the same deed, is refused (the third review).
            string askAfter = th.Answer("{\"id\":135,\"to\":\"sam\",\"day\":2,\"hour\":10,\"say\":\"Keep it to yourself, please.\"" + deed + "}").Result;
            // Its weight survives a turn that sends the game's own suspicion (the independent check).
            string withLevel = th.Answer("{\"id\":134,\"to\":\"sam\",\"day\":2,\"hour\":11,\"say\":\"Morning.\",\"suspicion\":0.2" + deed + "}").Result;
            Ok("a threat about the deed is reported once, never as an ask for silence, and only about a deed the game sent; its weight stays on the game's own suspicion",
               withLevel.Contains("\"suspicion\":0.35") &&
               threatOnce.Contains("\"threatened\":\"player.window_d1\"") && threatOnce.Contains("\"keepsQuiet\":null")
               && threatAgain.Contains("\"threatened\":null") && noDeed.Contains("\"threatened\":null") && askAfter.Contains("\"agreed\":false")
               && th.EngineFor("sam").Threatened.Contains("player.window_d1"), threatOnce + " | " + threatAgain);
        }
        // A THREAT THE WORDS MISS, READ BY THE CHECKING MODEL (Jafar, 30
        // September): read beside the reply for a line about a deed the words
        // did not find a threat in; found, it is reported as one the words
        // found is; no reading without a deed, for a line the words already
        // caught, or with the reading off.
        {
            string deed = ",\"deed\":{\"topic\":\"player.window_d1\",\"day\":1,\"hour\":23}";
            const string veiled = "Lovely shop you've got. Be a shame if the windows kept going in.";
            var yes = new ThreatFake { Says = true };
            var ty = new Helper(yes, TimeSpan.FromSeconds(8));
            LoadCards(ty, cardsDir); LoadCast(ty, cardsDir);
            string found = ty.Answer("{\"id\":141,\"to\":\"sam\",\"day\":2,\"hour\":10,\"say\":\"" + veiled + "\"" + deed + "}").Result;
            int afterFound = yes.Reads;
            string noDeedRead = ty.Answer("{\"id\":142,\"to\":\"lena\",\"day\":2,\"hour\":10,\"say\":\"" + veiled + "\"}").Result;
            string words = ty.Answer("{\"id\":143,\"to\":\"lena\",\"day\":2,\"hour\":10,\"say\":\"Say a word and you'll regret it.\"" + deed + "}").Result;
            var no = new ThreatFake { Says = false };
            var tn = new Helper(no, TimeSpan.FromSeconds(8));
            LoadCards(tn, cardsDir); LoadCast(tn, cardsDir);
            string cleared = tn.Answer("{\"id\":144,\"to\":\"sam\",\"day\":2,\"hour\":10,\"say\":\"" + veiled + "\"" + deed + "}").Result;
            var readOff = new ThreatFake { Says = true };
            var to = new Helper(readOff, TimeSpan.FromSeconds(8)) { ThreatByModel = false };
            LoadCards(to, cardsDir); LoadCast(to, cardsDir);
            string unread = to.Answer("{\"id\":145,\"to\":\"sam\",\"day\":2,\"hour\":10,\"say\":\"" + veiled + "\"" + deed + "}").Result;
            Ok("a veiled threat the words miss is read by the checking model beside the reply and reported as a threat; none read without a deed, for a line the words caught, or with the reading off",
               found.Contains("\"threatened\":\"player.window_d1\"") && afterFound == 1 && ty.EngineFor("sam").Threatened.Contains("player.window_d1")
               && noDeedRead.Contains("\"threatened\":null") && words.Contains("\"threatened\":\"player.window_d1\"") && yes.Reads == 1
               && cleared.Contains("\"threatened\":null") && no.Reads == 1 && unread.Contains("\"threatened\":null") && readOff.Reads == 0,
               found + " | " + cleared + " | reads " + yes.Reads + "/" + no.Reads + "/" + readOff.Reads);
        }
        Ok("a card lent to somebody else does not lend them its name; its own person keeps theirs",
           trusting.EngineFor("zlata") != null && trusting.EngineFor("zlata").SpeakerName == "" && trusting.EngineFor("lena").SpeakerName == null);

        // TALK KEPT WITH THE GAME'S SAVE (town list 6r).
        string talkDir = Path.Combine(Path.GetTempPath(), "talkhelper-selftest-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(talkDir);
        try
        {
            string slot = Path.Combine(talkDir, "slot1.talk.json");
            var keeper = new Helper(new FakeLlm(), TimeSpan.FromSeconds(8));
            LoadCards(keeper, cardsDir);
            await keeper.Answer("{\"id\":41,\"to\":\"sam\",\"say\":\"I was at the pictures all night, honest.\"}");
            string saved = await keeper.Answer("{\"talk\":\"save\",\"path\":" + JsonSerializer.Serialize(slot) + "}");
            Ok("save writes every conversation beside the game's save", Str(saved, "talk") == "saved" && File.Exists(slot) && !File.Exists(slot + ".tmp"), saved);
            await keeper.Answer("{\"talk\":\"reset\"}");
            Ok("reset (a new game) forgets every conversation", keeper.EngineFor("sam") == null);
            string loaded = await keeper.Answer("{\"talk\":\"load\",\"path\":" + JsonSerializer.Serialize(slot) + "}");
            var back = keeper.EngineFor("sam");
            Ok("load puts them back: he still remembers what Tom told him",
               Str(loaded, "talk") == "loaded" && back != null && back.Memory.Events.Exists(e => e.Text.Contains("pictures all night")), loaded);
            await keeper.Answer("{\"id\":42,\"to\":\"lena\",\"say\":\"Morning.\"}");
            string missing = await keeper.Answer("{\"talk\":\"load\",\"path\":" + JsonSerializer.Serialize(Path.Combine(talkDir, "none.talk.json")) + "}");
            Ok("loading a save with no talk beside it forgets the abandoned timeline's",
               keeper.EngineFor("sam") == null && keeper.EngineFor("lena") == null && missing.Contains("\"missing\":true"), missing);
            string odd = await keeper.Answer("{\"talk\":\"save\",\"path\":" + JsonSerializer.Serialize(Path.Combine(talkDir, "game.sav")) + "}");
            Ok("it will not write anything but a .talk.json", odd.Contains("path-must-end-.talk.json") && !File.Exists(Path.Combine(talkDir, "game.sav")), odd);
            File.WriteAllText(Path.Combine(talkDir, "bad.talk.json"), "{ not json");
            string bad = await keeper.Answer("{\"talk\":\"load\",\"path\":" + JsonSerializer.Serialize(Path.Combine(talkDir, "bad.talk.json")) + "}");
            Ok("a damaged talk file loads nobody and says so, and the helper carries on", bad.Contains("unreadable") && keeper.EngineFor("sam") == null, bad);
            // A failed save leaves no talk in the slot, never an older timeline's.
            await keeper.Answer("{\"talk\":\"load\",\"path\":" + JsonSerializer.Serialize(slot) + "}");
            Directory.CreateDirectory(slot + ".tmp");
            string failedSave = await keeper.Answer("{\"talk\":\"save\",\"path\":" + JsonSerializer.Serialize(slot) + "}");
            Directory.Delete(slot + ".tmp");
            Ok("a save that fails removes the old talk from the slot, so a load finds none",
               failedSave.Contains("unwritable") && !File.Exists(slot), failedSave);
            await keeper.Answer("{\"id\":43,\"to\":\"sam\",\"say\":\"Morning.\"}");
            string badLoad = await keeper.Answer("{\"talk\":\"load\",\"path\":\"slot2.sav\"}");
            Ok("a load with a bad path still forgets the timeline it leaves", badLoad.Contains("path-must-end") && keeper.EngineFor("sam") == null, badLoad);
            // A save that cannot replace a file another program holds leaves the old
            // game's talk there; its stamp keeps it from ever being loaded.
            await keeper.Answer("{\"id\":44,\"to\":\"sam\",\"say\":\"I was at the pictures, honest.\"}");
            string stampedA = await keeper.Answer("{\"talk\":\"save\",\"path\":" + JsonSerializer.Serialize(slot) + ",\"stamp\":\"game-A\"}");
            await keeper.Answer("{\"talk\":\"reset\"}");
            // WINDOWS ONLY (28 September): the held file refuses the save only where
            // file-sharing locks are enforced; on the build machine's Linux core-test
            // runner the save went through and this check failed. The game ships on
            // Windows only.
            if (OperatingSystem.IsWindows())
            {
                string heldSave;
                using (var held = new FileStream(slot, FileMode.Open, FileAccess.Read, FileShare.Read))
                    heldSave = await keeper.Answer("{\"talk\":\"save\",\"path\":" + JsonSerializer.Serialize(slot) + ",\"stamp\":\"game-B\"}");
                string staleLoad = await keeper.Answer("{\"talk\":\"load\",\"path\":" + JsonSerializer.Serialize(slot) + ",\"stamp\":\"game-B\"}");
                string rightLoad = await keeper.Answer("{\"talk\":\"LOAD\",\"path\":" + JsonSerializer.Serialize(slot) + ",\"stamp\":\"game-A\"}");
                Ok("talk left behind by another game is never loaded into this one, and a command's case does not matter",
                   stampedA.Contains("saved") && heldSave.Contains("unwritable") && staleLoad.Contains("\"stale\":true") && rightLoad.Contains("\"people\":1"),
                   heldSave + " " + staleLoad + " " + rightLoad);
            }
            else
            {
                string rightLoad = await keeper.Answer("{\"talk\":\"LOAD\",\"path\":" + JsonSerializer.Serialize(slot) + ",\"stamp\":\"game-A\"}");
                Ok("a command's case does not matter, and a save carries its stamp (the held-file case needs Windows' file locks)",
                   stampedA.Contains("saved") && rightLoad.Contains("\"people\":1"), stampedA + " " + rightLoad);
            }
        }
        finally { try { Directory.Delete(talkDir, true); } catch (Exception) { } }

        Console.WriteLine($"talkhelper selftest: passed={passed}/{passed + failed} failed={failed}");
        return failed == 0 ? 0 : 1;
    }

    /// A model that writes its reply in two parts, a pause apart, and a claim
    /// check that calls anything about Dennis or the yard invented.
    sealed class StreamFake : IStreamingLlmClient
    {
        readonly string _reply;
        public TimeSpan Pause = TimeSpan.FromMilliseconds(400);
        int _drafts;
        public bool ThrowBeforeText;
        /// What every draft after the first says.
        public string Redraft = "Can't say I did.";
        /// Whether the first draft's stream was stopped before it finished.
        public bool Stopped;
        public StreamFake(string reply) { _reply = reply; }
        static bool IsCheck(LlmRequest r) => r.System != null && r.System.StartsWith("You read one line");
        static bool IsSecondLook(LlmRequest r) => r.System != null && r.System.StartsWith("You check details");
        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            // the check's second look: nothing it flagged is supported
            if (IsSecondLook(request))
                return Task.FromResult(new LlmResponse { Text = "{\"verdicts\":[{\"n\":1,\"supported\":false}]}", InputTokens = 300, OutputTokens = 10, Model = request.Model });
            if (IsCheck(request))
            {
                var line = request.Messages.Count > 0 ? request.Messages[request.Messages.Count - 1].Content : "";
                // only the fenced line, not what the character knows
                int open = line.IndexOf("LINE:\n<<<>>>\n", StringComparison.Ordinal);
                var said = open >= 0 ? line.Substring(open + 13) : line;
                int close = said.IndexOf("<<<>>>", StringComparison.Ordinal);
                if (close >= 0) said = said.Substring(0, close);
                bool bad = said.Contains("Dennis") || said.Contains("yard");
                return Task.FromResult(new LlmResponse { Text = bad ? "{\"specifics\":[{\"detail\":\"who did it\",\"kind\":\"person\",\"source\":\"none\"}]}" : "{\"specifics\":[]}", InputTokens = 300, OutputTokens = 10, Model = request.Model });
            }
            // the first draft is the reply; a second draft says nothing it could invent
            return Task.FromResult(new LlmResponse { Text = _drafts++ == 0 ? _reply : Redraft, InputTokens = 400, OutputTokens = 10, Model = request.Model });
        }
        public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default)
        {
            if (ThrowBeforeText) throw new LlmStreamBrokenException("Overloaded");
            bool first = _drafts++ == 0;
            var text = first ? _reply : Redraft;
            var cut = text.IndexOf(". ", StringComparison.Ordinal) + 2;
            onText(text.Substring(0, cut) + text.Substring(cut, 1));
            try { await Task.Delay(Pause, ct); }
            catch (OperationCanceledException) { if (first) Stopped = true; throw; }
            onText(text);
            return new LlmResponse { Text = text, StopReason = "end_turn", InputTokens = 400, OutputTokens = 20, Model = request.Model };
        }
    }
}
