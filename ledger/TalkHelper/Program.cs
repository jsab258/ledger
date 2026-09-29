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
        // A turn abandoned at the patience limit may still be unwinding; the
        // same character's next line waits for it (the independent check: a
        // late unwind disturbed the next turn's transcript).
        readonly Dictionary<ConversationEngine, Task> _unwinding = new Dictionary<ConversationEngine, Task>();
        // Where an early first sentence is written (the selftest listens here).
        public Action<string> Emit = line => { lock (Console.Out) { Console.Out.WriteLine(line); Console.Out.Flush(); } };
        // The claim check on a stand-in model too, for the selftest.
        public bool CheckAlways;

        public bool Online => _llm != null;

        public ConversationEngine EngineFor(string to) => _engines.TryGetValue(to, out var e) ? e : null;

        ConversationEngine NewEngine(CharacterCard card)
        {
            var engine = new ConversationEngine(_llm, card, new MemoryStore(card.Id), new KnowledgeBase(),
                new SuspicionTracker(), _cost);
            // THE CLAIM CHECK ON THE REAL MODEL (ClaimCheck.cs, 24 September):
            // every reply is read for claims the character's knowledge does
            // not support before it is said. Not on the stand-in models,
            // which answer only from memory already.
            if (_llm is AnthropicClient || CheckAlways) engine.Checker = _llm;
            return engine;
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
                _engines.Clear();
                _unwinding.Clear();
                // Trust is the game's to say again for the timeline it loads.
                lock (_trusts) _trusts.Clear();
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
                    foreach (var kv in _engines) people[kv.Key] = kv.Value.CaptureTalk();
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
                _engines[kv.Key] = engine;
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
            var heardHeSaid = new List<string>();
            bool acquaintanceSent = false, metHim = false, heardOfHim = false, fresh = false;
            bool? trustsSent = null;
            string callsHim = null;
            List<string> present = null;
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
                // WHO IS REALLY WITH THEM (town list 6ad), as cast ids, when the game knows.
                if (r.TryGetProperty("present", out v) && v.ValueKind == JsonValueKind.Array)
                {
                    present = new List<string>();
                    foreach (var pe in v.EnumerateArray()) if (pe.ValueKind == JsonValueKind.String) present.Add(pe.GetString());
                }
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
                        // How surely the naming reached them; a game that does not send it yet gets the account's own.
                        acc.NamingConfidence = a.TryGetProperty("namingConfidence", out var nc) && nc.ValueKind == JsonValueKind.Number ? nc.GetDouble() : acc.Confidence;
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
                // HOW THIS PERSON KNOWS TOM (town list 6s), as the game knows it:
                // whether they have met him, heard of him, and what they call him.
                if (r.TryGetProperty("acquaintance", out var aq) && aq.ValueKind == JsonValueKind.Object)
                {
                    acquaintanceSent = true;
                    metHim = Bool(aq, "met");
                    heardOfHim = Bool(aq, "heardOf");
                    callsHim = aq.TryGetProperty("calls", out var ac) && ac.ValueKind == JsonValueKind.String ? ac.GetString() : null;
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
            if (talkOp != null) return await Talk(talkOp, talkPath, talkStamp);
            if (walkedFrom != null)
            {
                bool already;
                lock (_walkedHandled) already = _walkedHandled.Remove(walkedFrom);
                if (already) return JsonSerializer.Serialize(new { walkedAway = walkedFrom, noted = true }, Plain);
                var left = EngineFor(walkedFrom);
                if (left != null) left.WalkedAway(walkedHeard, new GameTime(day, hour, minute));
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
                _engines[key] = engine;
            }
            // A card lent to somebody else: their name is not the card's
            // (town list 6be, the independent check).
            engine.SpeakerName = key != to ? "" : null;
            // WHO THEY KNOW, AND WHERE (town list 6ad), from the cast file this hour.
            if (Cast != null) engine.People = Cast.PeopleFor(key, day, hour, present);
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
            if (fresh) { engine.StartFresh(); engine.GameMarksFresh = true; }
            // Kept until the game sends it again; until the game has ever sent it,
            // read off this conversation's own earlier talk with him.
            // Met is the game's word or their own earlier talk: the game cannot
            // make them forget a conversation they have had.
            // NAMED ONLY ON TRUST (Jafar, 29 September page): Sheila keeps him
            // at "the new owner", her "new management", until the game says she
            // trusts him, whatever name its ladder sends; what it said holds
            // until it says otherwise (the independent check).
            if (trustsSent.HasValue) lock (_trusts) _trusts[key] = trustsSent.Value;
            bool trustsHim;
            lock (_trusts) trustsHim = _trusts.TryGetValue(key, out var tv) && tv;
            if (acquaintanceSent && !trustsHim && Cast != null && Cast.NamesHimOnlyOnTrust(key)) callsHim = null;
            if (acquaintanceSent)
            {
                engine.HowYouKnowHim = Tom.HowTheyKnowHim(metHim || engine.HasSpokenWithHim, heardOfHim, callsHim, onlyTheirOwnTalk: !metHim);
                engine.KnowsHimFromGame = true;
            }
            else if (!engine.KnowsHimFromGame)
                engine.HowYouKnowHim = Tom.HowTheyKnowHim(engine.HasSpokenWithHim, false, null, onlyTheirOwnTalk: true);
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
            // Only the deed this line is sent with: an older deed would come without
            // its gravity (the independent check: a killing kept quiet).
            string silenceTopic = deedTopic;
            if (silenceTopic != null && !string.IsNullOrEmpty(say))
            {
                if (Silence.OwnsUp(say) && engine.HeardOwnUp(silenceTopic, now)) ownedUpOut = silenceTopic;
                if (Silence.AsksQuiet(say))
                {
                    var stance = Cast?.QuietStance(key) ?? KeepsQuietFor.Friend;
                    var ident = new PlayerIdentity();
                    bool firstName = callsHim != null && (callsHim == ident.First || callsHim == ident.Diminutive);
                    engine.HeardAskQuiet(silenceTopic, Silence.Agrees(stance, firstName, deedGrave), now);
                    bool agreed = engine.KeepsQuiet[silenceTopic];
                    keepsQuietOut = new { topic = silenceTopic, agreed, fragile = agreed && Silence.Fragile(stance) };
                }
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

            if (_llm == null)
                return JsonSerializer.Serialize(new { id, to, day, reply = brush, ms = 0L, offline = true, timedOut = false, paused = AiNotice.TalkOff, heard, suspicion = holds, level, why = suspicionWhy ?? engine.Suspicion.LatestReason(), manner, ownedUp = ownedUpOut, keepsQuiet = keepsQuietOut }, Plain);
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
            using (var cts = new CancellationTokenSource(_patience))
            {
                try
                {
                    Func<string, Task<bool>> onFirst = null;
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
                    var task = engine.SayToAsync(say, now, scene, cts.Token, onFirst);
                    var walkedOff = Task.Delay(Timeout.Infinite, walkCts.Token).ContinueWith(_ => { }, TaskScheduler.Default);
                    var done = await Task.WhenAny(task, Task.Delay(_patience), walkedOff);
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
                        return JsonSerializer.Serialize(new { id, to, walkedOff = true }, Plain);
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
            bool generated = reply != brush && !fellBack && !ResponseValidator.IsDeflection(reply, card.Name);
            string model = generated ? engine.Model : null;
            Keep(new Turn { Id = id, To = to, Day = day, Hour = hour, Minute = minute, Say = say, Reply = reply, Generated = generated,
                            Model = model, Invented = invented, Unchecked = @unchecked, Ms = sw.ElapsedMilliseconds });
            // ENDED: the character closed the conversation (town list 6ae).
            bool ends = !timedOut && engine.LastEnded;
            return JsonSerializer.Serialize(new { id, to, day, reply, rest, ms = sw.ElapsedMilliseconds, offline = false, timedOut, paused, ends, heard, suspicion = holds, level, why = suspicionWhy ?? engine.Suspicion.LatestReason(), manner, invented, promised, spokeOf, putToHim, named, went, claim = claimOut, ownedUp = ownedUpOut, keepsQuiet = keepsQuietOut, @unchecked, fellBack, generated, model }, Plain);
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
        // THROUGH OUR RELAY (town list 6b): --relay <address> and a copy's code
        // (--copy or LEDGER_COPY) instead of a key, so no key ships with the game.
        int ri = Array.IndexOf(args, "--relay"), ci = Array.IndexOf(args, "--copy");
        string relay = ri >= 0 && ri + 1 < args.Length ? args[ri + 1] : null;
        string copy = ci >= 0 && ci + 1 < args.Length ? args[ci + 1] : Environment.GetEnvironmentVariable("LEDGER_COPY");
        ILlmClient llm = fake ? new KnowledgeFake()
            : relay != null ? (string.IsNullOrEmpty(copy) ? null : new AnthropicClient(null) { BaseUrl = relay, CopyCode = copy })
            : (string.IsNullOrEmpty(key) ? null : new AnthropicClient(key));
        var helper = new Helper(llm, TimeSpan.FromSeconds(8));
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
        LoadCards(helper, CardsDir(args));
        LoadCast(helper, CardsDir(args));
        Console.Out.WriteLine(JsonSerializer.Serialize(new { ready = true, cards = helper.Cards.Keys, online = helper.Online, fake, notice = new { title = AiNotice.Title, text = AiNotice.TextFor(relay != null), report = AiNotice.ReportLabel } }, Plain));
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
        while (true)
        {
            string line;
            if (waiting.Count > 0) line = waiting.Dequeue();
            else if (!incoming.TryTake(out line, Timeout.Infinite)) break;
            if (line.Trim().Length == 0) continue;
            var answer = helper.Answer(line);
            while (!answer.IsCompleted)
            {
                if (incoming.TryTake(out var next, 50)) { helper.WalkOffIfFor(next); waiting.Enqueue(next); }
                else if (incoming.IsCompleted) break;
            }
            Console.Out.WriteLine(await answer);
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

    // A stand-in model that says the next of its lines each call, then the last again.
    sealed class ScriptFake : ILlmClient
    {
        readonly Queue<string> _lines;
        string _last = "Right.";
        public ScriptFake(params string[] lines) => _lines = new Queue<string>(lines);
        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
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
            var eh = new Helper(llm, patience) { Early = true, CheckAlways = true };
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

        var clean = await Early(new StreamFake("Aye. I saw him go by the chip shop at nine."), "See anything?", TimeSpan.FromSeconds(8));
        Ok("the checked first sentence goes out before the rest is written",
           clean.firsts.Count == 1 && Str(clean.firsts[0].line, "first") == "Aye." && clean.firsts[0].at + 250 < clean.lastAt,
           clean.firsts.Count + " " + clean.lastAt);
        Ok("and the rest follows, to be spoken after it", Str(clean.last, "rest") == "I saw him go by the chip shop at nine." &&
           Reply(clean.last) == "Aye. I saw him go by the chip shop at nine.", clean.last);

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
