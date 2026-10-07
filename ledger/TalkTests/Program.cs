using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

namespace Ledger.TalkTests
{
    /// THE TALK'S OWN TESTS (the talk task of 7 October 2026), framework-free like
    /// CoreTests: each check throws on failure; exit code 0 means every one passed.
    ///
    ///     dotnet run --project ledger/TalkTests -c Release
    ///
    /// What they hold the talk to, each written from what the game should do
    /// before the code that does it:
    ///   - THE LADDER: a character whose reply the check refuses twice does not
    ///     say "that's all I know" while they still know something that bears on
    ///     his question. They climb: the next relevant fact they know, said in
    ///     its plain words; then whom to ask; then who told them; and only then a
    ///     refusal in their own voice, with a reason. Nothing on it is the model's.
    ///   - WHAT EACH CHARACTER HAS TOLD EACH LISTENER, kept and saved, so nothing
    ///     is told twice.
    ///   - WHO TOLD ME: every retelling of a rumour records who told the hearer,
    ///     as well as who first saw it, through saves, so a character can say
    ///     "Sheila told me".
    static class Program
    {
        static int _passed;

        static void Check(bool condition, string name, string detail = null)
        {
            if (!condition) throw new Exception($"FAILED: {name}" + (detail == null ? "" : $" — {detail}"));
            _passed++;
            Console.WriteLine($"  ok - {name}");
        }

        static async Task<int> Main()
        {
            try
            {
                TestOwnLines();
                TestFrameBreaks();
                TestRealNames();
                await TestLadder();
                await TestTold();
                TestRumourTeller();
                TestAccountNamesTeller();
                await TestCapPrices();
                Console.WriteLine($"\nALL {_passed} TALK CHECKS PASSED");
                return 0;
            }
            catch (Exception e)
            {
                Console.WriteLine(e.Message);
                Console.WriteLine(e.StackTrace);
                return 1;
            }
        }

        // ------------------------------------------------------------ helpers

        /// A model that answers from a script, in order, the last line again
        /// once the script is spent; every request kept.
        sealed class ScriptedLlm : ILlmClient
        {
            readonly Queue<string> _lines;
            public readonly List<LlmRequest> Requests = new List<LlmRequest>();
            public ScriptedLlm(params string[] lines) => _lines = new Queue<string>(lines);
            public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
            {
                Requests.Add(request);
                var text = _lines.Count > 1 ? _lines.Dequeue() : _lines.Peek();
                return Task.FromResult(new LlmResponse { Text = text, StopReason = "end_turn", InputTokens = 10, OutputTokens = 10, Model = request.Model });
            }
        }

        static string RepoRoot()
        {
            var dir = new DirectoryInfo(AppContext.BaseDirectory);
            while (dir != null && !Directory.Exists(Path.Combine(dir.FullName, "production", "cast", "cards"))) dir = dir.Parent;
            if (dir == null) throw new Exception("FAILED: the repository's cast cards were not found above " + AppContext.BaseDirectory);
            return dir.FullName;
        }

        /// A talking card as the talk program loads it: the card, and the
        /// street's plain facts given to it (StreetFacts.AddTo).
        static CharacterCard Card(string id) =>
            StreetFacts.AddTo(CharacterCard.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "cast", "cards", id + ".md"))), id);

        /// The check's id for one of the card's hard facts (H1 is the first),
        /// as ClaimCheck.KnownItems numbers them.
        static string H(CharacterCard card, string fact)
        {
            int i = card.HardFacts.IndexOf(fact);
            if (i < 0) throw new Exception("FAILED: the card does not hold " + fact);
            return "H" + (i + 1);
        }

        static string List(params (string detail, string source)[] specifics) =>
            "{\"specifics\": [" + string.Join(", ", specifics.Select(s =>
                "{\"detail\": \"" + s.detail + "\", \"kind\": \"action\", \"source\": \"" + s.source + "\"}")) + "]}";

        const string Unsupported = "{\"verdicts\": [{\"n\": 1, \"supported\": false}]}";
        const string Clean = "{\"specifics\": []}";
        static readonly GameTime Now = new GameTime(1, 10, 0);
        const string Scene = "Dry, grey. Where you are: the front room of Mickey's, the cab office.";

        static ConversationEngine Engine(string id, ILlmClient talk, ILlmClient check, MemoryStore memory = null) =>
            new ConversationEngine(talk, Card(id), memory ?? new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker(), new CostTracker()) { Checker = check };

        /// One turn whose two drafts the check both refuses, each draft's list
        /// citing `cited` for a detail it supports and none for the one it
        /// refuses (the second look refusing that one): the way a reply that
        /// reaches for a true fact and adds texture nobody wrote is refused.
        static (ScriptedLlm talk, ILlmClient check) RefusedTwice(string cited)
        {
            var talk = new ScriptedLlm("The keys are kept close, and the phone's been ringing all morning.",
                                       "Somebody has the keys, and a fella came by about the rank.");
            var first = cited == null ? List(("the phone has been ringing all morning", "none"))
                                      : List(("Sheila keeps the keys", cited), ("the phone has been ringing all morning", "none"));
            var second = cited == null ? List(("a fella came by about the rank", "none"))
                                       : List(("Sheila has the keys", cited), ("a fella came by about the rank", "none"));
            return (talk, new CheckLlm(first, second));
        }

        /// The check, scripted: each list in turn for the list calls, and every
        /// second look refusing its detail, however many the lists flagged.
        sealed class CheckLlm : ILlmClient
        {
            readonly Queue<string> _lists;
            public CheckLlm(params string[] lists) => _lists = new Queue<string>(lists);
            public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
            {
                bool look = request.System != null && request.System.StartsWith("You check details against", StringComparison.Ordinal);
                var text = look ? Unsupported : _lists.Count > 1 ? _lists.Dequeue() : _lists.Peek();
                return Task.FromResult(new LlmResponse { Text = text, StopReason = "end_turn", InputTokens = 10, OutputTokens = 10, Model = request.Model });
            }
        }

        static async Task<string> RefusedTurn(ConversationEngine e, string said, string cited)
        {
            var (talk, check) = RefusedTwice(cited);
            Swap(e, talk, check);
            return await e.SayToAsync(said, Now, Scene);
        }

        // The engine keeps its model; the tests give each turn its own script
        // through a client that hands every call to whichever script is current.
        sealed class Relay : ILlmClient
        {
            public ILlmClient To;
            public Task<LlmResponse> CompleteAsync(LlmRequest r, CancellationToken ct = default) => To.CompleteAsync(r, ct);
        }
        static readonly Dictionary<ConversationEngine, (Relay talk, Relay check)> Relays = new Dictionary<ConversationEngine, (Relay, Relay)>();

        static ConversationEngine Relayed(string id, MemoryStore memory = null)
        {
            var talk = new Relay { To = new ScriptedLlm("...") };
            var check = new Relay { To = new ScriptedLlm(Clean) };
            var e = Engine(id, talk, check, memory);
            Relays[e] = (talk, check);
            return e;
        }

        static void Swap(ConversationEngine e, ILlmClient talk, ILlmClient check)
        {
            var (t, c) = Relays[e];
            t.To = talk;
            c.To = check;
        }

        // ------------------------------------------------------------ the lines

        static void TestOwnLines()
        {
            Console.WriteLine("The ladder's own lines, on every card that talks:");
            foreach (var id in new[] { "lena", "rocco", "sam" })
            {
                var card = Card(id);
                var ask = card.Own("ask");
                var told = card.Own("told");
                var refuse = card.Own("refuse");
                Check(ask.Count >= 2 && ask.All(l => l.Contains("{who}")), id + ": at least two ways of saying whom to ask, each naming them", string.Join(" | ", ask));
                Check(told.Count >= 2 && told.All(l => l.Contains("{who}")), id + ": at least two ways of saying who told them, each naming them", string.Join(" | ", told));
                Check(refuse.Count >= 2, id + ": at least two refusals with a reason", string.Join(" | ", refuse));
                foreach (var line in ask.Concat(told).Concat(refuse))
                {
                    var said = line.Replace("{who}", "June");
                    Check(ContentRule.SpeechBreaks(said) == null && SafetyRule.SpeechBreaks(said) == null && RealWorld.Find(said).Count == 0
                          && !ClaimCheck.IsKnownOnly(said, card) && Promises.Find(said).Count == 0,
                          id + ": passes the content rule, names nothing real, is no \"that's all I know\" and promises nothing: " + said);
                    var shown = ResponseValidator.Validate(said, card.Name, card.AlsoCalled);
                    Check(!ResponseValidator.IsDeflection(shown, card.Name), id + ": the reply guard lets it through as speech: " + said, shown);
                }
            }
            // Somebody with no lines of their own still climbs, in the shared words.
            var bare = CharacterCard.Parse("# Hal\nid: hal\ntier: ambient\n\n## Summary\nKeeps the coin shop.\n");
            Check(TalkLadder.LineFor(bare, "ask", 0, "Sheila").Contains("Sheila") && TalkLadder.LineFor(bare, "told", 0, "Sheila").Contains("Sheila")
                  && TalkLadder.LineFor(bare, "refuse", 0, null).Length > 0,
                  "a card without the ladder's lines has the shared ones");
        }

        // ------------------------------------------------------------ the frame

        static void TestFrameBreaks()
        {
            Console.WriteLine("Never a word about playing a part:");
            // The bait of 7 October: Darren, asked for a verse for his funeral.
            foreach (var line in new[]
            {
                "I need to stay in character here. You're asking me something that doesn't fit where I am.",
                "Breaking character for a second, I can't do that.",
                "That's a bit out of character for my character, mate.",
            })
                Check(ResponseValidator.IsDeflection(ResponseValidator.Validate(line, "Darren Milner"), "Darren Milner"),
                      "talk of staying in character is never said: " + line);
            Check(!ResponseValidator.IsDeflection(ResponseValidator.Validate("That's not like Ron, that.", "Darren Milner"), "Darren Milner"),
                  "a person's ordinary words about somebody are said");
        }

        // ------------------------------------------------------------ real names

        static void TestRealNames()
        {
            Console.WriteLine("Nothing real named, not even to deny it:");
            // The bait of 7 October: the four replies that named something real.
            foreach (var (line, name) in new[]
            {
                ("I'm a docker from the Hook, friend. Don't know much about Shakespeare.", "Shakespeare"),
                ("Politics isn't what moves on Quay Street. The fella in Westminster doesn't change whether Ron's got a fare.", "Westminster"),
                ("I've not been to London. Haven't had call to go there.", "London"),
                ("You after something that comes from London way, or just making talk?", "London"),
                ("We went to Blackpool once, before the docks went.", "Blackpool"),
                ("Never read Dickens in my life.", "Dickens"),
                ("He's gone over to Hull for the week.", "Hull"),
            })
                Check(RealWorld.Find(line).Contains(name), "a real place or writer is found: " + name, string.Join(", ", RealWorld.Find(line)));
            foreach (var line in new[]
            {
                "There's a hole in the hull of that boat.", "A hot bath and an early night.", "Reading the paper's all I do.",
                "Down south, somewhere. Never been.", "Quay Street, the Hook, Copper Row over the water.", "Father Walsh came over from Ireland.",
                "The Madonna in the chapel.", "Takes courage, that.", "The mobile library comes Thursdays.",
            })
                Check(RealWorld.Find(line).Count == 0, "an ordinary word, or the town's own places, is not: " + line, string.Join(", ", RealWorld.Find(line)));
            Check(RealWorld.PromptRule.Contains("never been there") && RealWorld.PromptRule.Contains("poem")
                  && RealWorld.PromptRule.Contains("sing") && RealWorld.PromptRule.Contains("city"),
                  "the talk's rule names real places, writers, songs and poems, and saying you never went is still naming it");
        }

        // ------------------------------------------------------------ the ladder

        static async Task TestLadder()
        {
            Console.WriteLine("The ladder before \"that's all I know\":");
            ConversationEngine.Ladder = true;
            try
            {
                var ron = Card("rocco");
                string door = StreetFacts.Held("door", "rocco");
                string doorSaid = StreetFacts.SaidFor(door);

                // 1. The next relevant fact he knows, said plainly.
                var e = Relayed("rocco");
                string first = await RefusedTurn(e, "Who's got the keys to this place?", H(ron, door));
                Check(first.EndsWith(doorSaid) && e.LastRung == "fact" && e.LastSaidPlainly && !ClaimCheck.IsKnownOnly(first, e.Card),
                      "refused twice, he says the fact his drafts reached for, in its plain words, not \"that's all I know\"", first);
                Check(e.LastWouldHaveSaid != null && ClaimCheck.IsKnownOnly(e.LastWouldHaveSaid, e.Card),
                      "and what today's talk would have said is kept beside it, for measuring", e.LastWouldHaveSaid);
                Check(e.HasTold("player", door), "and he has now told the player that fact");

                // 2. Asked again: not the same fact twice; whom to ask (the fact is Sheila's).
                string second = await RefusedTurn(e, "Anyone else have a key?", H(ron, door));
                Check(!second.Contains(doorSaid) && second.Contains("Sheila") && e.LastRung == "ask",
                      "asked again, he does not repeat himself: he says whom to ask", second);

                // 3. And again: nothing left to give, a refusal with a reason, in his own words.
                string third = await RefusedTurn(e, "Come on, who else?", H(ron, door));
                Check(e.LastRung == "refuse" && e.Card.Own("refuse").Contains(third) && !ClaimCheck.IsKnownOnly(third, e.Card),
                      "and again: he refuses, with a reason, in his own words", third);

                // 4. Nothing relevant at all: an honest "don't know", never a refusal that
                // pretends he is keeping something back, and never a fact by shared words.
                var none = Relayed("rocco");
                string nothing = await RefusedTurn(none, "What did Mickey keep in the safe?", null);
                string nothingAgain = await RefusedTurn(none, "Go on, what was in the safe?", null);
                Check(none.LastRung == null && ClaimCheck.IsKnownOnly(nothing, none.Card) && ClaimCheck.IsKnownOnly(nothingAgain, none.Card) && !none.LastSaidPlainly,
                      "with nothing relevant to give, he says he does not know, asked once or twice; the refusal is only ever the top of a climb", nothing + " | " + nothingAgain);

                // 5. Who told them: a story heard from somebody, the teller named.
                var mem = new MemoryStore("sam");
                mem.Append(new MemoryEvent(new GameTime(0, 21, 0), "heard", 0.8, "I heard from Ada that a man ran from Rita's window towards the quay."));
                var darren = Relayed("sam", mem);
                string heard = await RefusedTurn(darren, "What happened at Rita's?", "M1");
                Check(darren.LastRung == "told" && heard.Contains("Ada") && !heard.Contains("quay"),
                      "a story he only heard: he names who told him, and adds nothing of it his drafts were refused for", heard);
                string after = await RefusedTurn(darren, "Who else knows about it?", "M1");
                Check(darren.LastRung == "refuse", "and does not name them twice", after);

                // 6. A secret is never said plainly, however the drafts reached for it.
                var sheila = Card("lena");
                string secret = sheila.HardFacts.First(f => f.Contains("second book"));
                var keeps = Relayed("lena");
                string kept = await RefusedTurn(keeps, "Where are the real books?", H(sheila, secret));
                Check(!kept.Contains("second book") && !kept.Contains("real one") && !kept.Contains("know where") && keeps.LastRung == null
                      && ClaimCheck.IsKnownOnly(kept, keeps.Card),
                      "her secret, though her drafts reached for it, is never said plainly", kept + " rung=" + keeps.LastRung + " invented=" + string.Join("|", keeps.LastInvented) + " again=" + string.Join("|", keeps.LastRefusedAgain));

                // 7. A fact about the speaker is hers to say, and nobody to point to.
                var own = Relayed("lena");
                string doorHers = StreetFacts.Held("door", "lena");
                string ownLine = await RefusedTurn(own, "Who's got the keys?", H(sheila, doorHers));
                string ownAgain = await RefusedTurn(own, "Who else, then?", H(sheila, doorHers));
                Check(ownLine.EndsWith(StreetFacts.SaidFor(doorHers)) && own.LastRung == "refuse" && !ownAgain.Contains("Sheila"),
                      "her own fact in her own words; asked again she never sends him to herself", ownLine + " | " + ownAgain);

                // 6b. What the drafts reached for must bear on his words: asked for a poem,
                // a draft that wandered to the locked door does not make the door the answer
                // (the bait of 7 October: "Know any poems?" answered with Mickey's room).
                var poem = Relayed("lena");
                string recite = await RefusedTurn(poem, "Know any poems? Recite one for me.", H(sheila, StreetFacts.Held("door", "lena")));
                Check(poem.LastRung == null && ClaimCheck.IsKnownOnly(recite, poem.Card),
                      "a fact the drafts cited that shares nothing with his question is no answer to it", recite);
                Check(ClaimCheck.SharesTellingWord("Who's got the keys to this place?", StreetFacts.Held("door", "lena"))
                      && ClaimCheck.SharesTellingWord("Did Mickey live round here?", StreetFacts.Held("flat", "lena"))
                      && !ClaimCheck.SharesTellingWord("Which cars are still on the road?", StreetFacts.Held("office", "lena"))
                      && !ClaimCheck.SharesTellingWord("Morning.", StreetFacts.Held("hours", "lena")),
                      "a telling word shared: keys and key, live and living; never a greeting or the time of day");

                // 6c. A word half of what they know shares ("street", "Mickey") is no
                // sign a fact bears on his question (the fresh set of 7 October: "What's
                // the street like after dark?" answered with the cafe's hours).
                var corpus = ClaimCheck.KnownItems(sheila, null, null, null, Scene, Now.ToldAs).Select(i => i.text).ToList();
                for (int i = 0; i < 12; i++) corpus.Add("Quay Street and Mickey, item " + i + ".");
                Check(!ClaimCheck.SharesTellingWord("What's the street like after dark?", StreetFacts.Held("cafe", "lena"), corpus)
                      && ClaimCheck.SharesTellingWord("Who's got the keys to this place?", StreetFacts.Held("door", "lena"), corpus),
                      "a shared word counts only when it is not in a fifth of all they know");

                // 7a. Her own introduction, said to another question, without her name
                // in front of it ("Sheila Dunn. I keep the books ..." read as a recital).
                var bookTalk = Relayed("lena");
                string ownBooks = StreetFacts.Held("sheila_books", "lena");
                string look = await RefusedTurn(bookTalk, "Can I have a look at the books?", H(sheila, ownBooks));
                Check(bookTalk.LastRung == "fact" && look.EndsWith("I keep the books at Mickey's, and have for thirty-one years.") && !look.Contains("Sheila Dunn"),
                      "her own job, said to another question, comes without her name", look);

                // 7b. Somebody else's job is a pointer, not an answer: asked what Sheila
                // thinks of him, Ron sends him to her rather than saying she keeps the
                // books; asked who she is, he says it.
                string books = StreetFacts.Held("sheila_books", "rocco");
                var pointer = Relayed("rocco");
                string thinks = await RefusedTurn(pointer, "What does Sheila really think of me?", H(ron, books));
                Check(pointer.LastRung == "ask" && thinks.Contains("Sheila") && !thinks.Contains("books"),
                      "a fact that is only somebody else's job sends him to them", thinks);
                var who = Relayed("rocco");
                string whoIs = await RefusedTurn(who, "Who's Sheila?", H(ron, books));
                Check(who.LastRung == "fact" && whoIs.EndsWith(StreetFacts.SaidFor(books)),
                      "asked who they are, he says it", whoIs);
                Check(who.LastLeads.Count == 1 && who.LastLeads[0].StartsWith("fact|") && pointer.LastLeads[0].StartsWith("ask|"),
                      "and each turn's leads are kept, for reading a run", string.Join(" / ", who.LastLeads) + " | " + string.Join(" / ", pointer.LastLeads));

                // 8. The rule table's choice still leads, as measured on 30 September.
                ConversationEngine.UseRules = true;
                ConversationEngine.PlainFallback = true;
                try
                {
                    var bed = Relayed("lena");
                    string sleep = await RefusedTurn(bed, "Where do I sleep?", null);
                    Check(sleep.EndsWith("You're in Mickey's flat, over the office.") && bed.LastRung == "fact",
                          "a question the rule table knows: its fact first, said plainly", sleep);
                    // A partial answer says whom to ask for the rest in the same line, as
                    // measured on 30 September; pressed on it, he has given all he has.
                    var money = Relayed("rocco");
                    string takings = await RefusedTurn(money, "Is there any money in the business?", null);
                    string pressed = await RefusedTurn(money, "Is the business doing all right, though?", null);
                    // The rule table's chosen facts are its answer, never turned into pointers:
                    // asked who runs things, Darren's second rung says Sheila keeps the books.
                    var runs = Relayed("sam");
                    string r1 = await RefusedTurn(runs, "Who runs things round here?", null);
                    string r2 = await RefusedTurn(runs, "Who runs things, though?", null);
                    Check(r1.Contains("Mickey left you the office") && r2.Contains("keeps the books") && runs.LastRung == "fact",
                          "the rule table's facts are said as its answer, one a turn, a job fact among them", r1 + " | " + r2);
                    Check(takings.Contains("Trade's been thin.") && takings.Contains("Sheila") && money.LastRung == "refuse"
                          && !pressed.Contains("Trade's been thin.") && !pressed.Contains("Sheila"),
                          "a partial answer with whom to ask for the rest; pressed, nothing said twice", takings + " | " + pressed);
                }
                finally { ConversationEngine.UseRules = false; ConversationEngine.PlainFallback = false; }

                // 9. The first turn's prompt is exactly today's: the ladder changes
                // only what is said when both drafts are refused, so one run
                // measures both (the paired bench).
                ConversationEngine.Ladder = false;
                string today = Relayed("lena").BuildSystemPrompt("Who's got the keys?", Now, Scene);
                ConversationEngine.Ladder = true;
                string withLadder = Relayed("lena").BuildSystemPrompt("Who's got the keys?", Now, Scene);
                Check(today == withLadder, "with nothing yet told, the prompt is word for word today's");
            }
            finally { ConversationEngine.Ladder = false; }

            // 10. With the ladder off, nothing changes: "that's all I know", as today.
            var off = Relayed("rocco");
            string stock = await RefusedTurn(off, "Who's got the keys to this place?", H(Card("rocco"), StreetFacts.Held("door", "rocco")));
            Check(ClaimCheck.IsKnownOnly(stock, off.Card) && off.LastRung == null, "with the ladder off, today's line", stock);
        }

        // ------------------------------------------------------------ what was told

        static async Task TestTold()
        {
            Console.WriteLine("What each character has told each listener:");
            ConversationEngine.Ladder = true;
            try
            {
                var ron = Card("rocco");
                string drivers = StreetFacts.Held("drivers", "rocco");
                // A reply of the model's own that the check passes, drawing on a fact.
                var e = Relayed("rocco");
                Swap(e, new ScriptedLlm("Two drivers, boss, one days and one nights."),
                        new ScriptedLlm(List(("two drivers, one by day and one by night", H(ron, drivers)))));
                string said = await e.SayToAsync("How many drivers are there?", Now, Scene);
                Check(said.StartsWith("Two drivers") && e.HasTold("player", drivers),
                      "a fact his own checked reply drew on is counted as told", said);
                Check(!e.HasTold("ada", drivers), "told to the player is not told to anybody else");

                // Asked later, refused twice and reaching for it again: not said again.
                string again = await RefusedTurn(e, "Who drives for us?", H(ron, drivers));
                Check(!again.Contains(StreetFacts.SaidFor(drivers)) && e.LastRung != "fact",
                      "a fact he has told him is not said plainly to him again", again);

                // The next prompt says what he has told him already.
                string prompt = e.BuildSystemPrompt("Anything else?", Now, Scene);
                Check(prompt.Contains("already told him") && prompt.Contains(drivers),
                      "and the next reply is written knowing what he has already told him");

                // Kept with the talk: a reload remembers it; another listener's is their own.
                e.Listener = "ada";
                Swap(e, new ScriptedLlm("Two drivers, love."), new ScriptedLlm(List(("two drivers", H(ron, drivers)))));
                await e.SayToAsync("How many drivers?", Now, Scene);
                e.Listener = "player";
                var saved = e.CaptureTalk();
                var back = Relayed("rocco");
                back.RestoreTalk(saved);
                Check(back.HasTold("player", drivers) && back.HasTold("ada", drivers) && !back.HasTold("player", StreetFacts.Held("cafe", "rocco")),
                      "what was told, to whom, survives a save");
                back.RestoreTalk(null);
                Check(!back.HasTold("player", drivers), "and an empty save forgets it");
                var older = Relayed("rocco");
                saved.Remove("told");
                older.RestoreTalk(saved);
                Check(!older.HasTold("player", drivers), "a save from before it was kept reads as nothing told");
            }
            finally { ConversationEngine.Ladder = false; }
        }

        // ------------------------------------------------------------ the key's cap

        /// A model that answers as the API does: under the dated name of the model asked for.
        sealed class DatedLlm : ILlmClient
        {
            public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default) =>
                Task.FromResult(new LlmResponse { Text = "ok", StopReason = "end_turn", InputTokens = 1_000_000, OutputTokens = 0,
                                                  Model = request.Model == Models.Ambient ? "claude-haiku-4-5-20251001" : request.Model });
        }

        static async Task TestCapPrices()
        {
            Console.WriteLine("The key's cap charges each call at its own model's price:");
            var cap = new BudgetedClient(new DatedLlm(), 100);
            await cap.CompleteAsync(new LlmRequest { Model = Models.Ambient, MaxTokens = 0 });
            Check(Math.Abs(cap.SpentUsd - Models.Cost[Models.Ambient].inPerM) < 1e-6,
                  "a million tokens in to Haiku 4.5, answered under its dated name, costs Haiku's dollar, not the dearest rate", cap.SpentUsd.ToString("0.0000"));
        }

        // ------------------------------------------------------------ who told me

        static GossipMill Mill(params (string id, string name)[] people)
        {
            var g = new SocialGraph();
            for (int i = 0; i + 1 < people.Length; i++) g.Link(people[i].id, people[i + 1].id, 0.9);
            var mill = new GossipMill(g);
            foreach (var (id, name) in people) mill.Add(new Gossiper(id, name, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker()));
            return mill;
        }

        static void TestRumourTeller()
        {
            Console.WriteLine("Who told me, through every retelling:");
            var mill = Mill(("rita", "Rita"), ("lena", "Sheila"), ("rocco", "Ron"));
            var window = new Fact("player", "window_d1", "seen");
            mill.Witness("rita", window, "the man that did the window ran towards the quay", true, new GameTime(1, 23, 0), 0.9, rung: 2);
            mill.Tick(new GameTime(1, 23, 6), (a, b) => true);
            mill.Tick(new GameTime(1, 23, 12), (a, b) => true);
            var own = mill.Get("rita").Best("player.window_d1");
            var sheila = mill.Get("lena").Best("player.window_d1");
            var ron = mill.Get("rocco").Best("player.window_d1");
            Check(own.ToldById == null, "who saw it was told by nobody");
            Check(sheila != null && sheila.ToldById == "rita" && sheila.OriginId == "rita", "the first hearer was told by the witness",
                  sheila == null ? "not heard" : sheila.ToldById);
            Check(ron != null && ron.ToldById == "lena" && ron.OriginId == "rita" && ron.Hops == 2,
                  "the next was told by the first hearer, and the story still says who first saw it", ron == null ? "not heard" : ron.ToldById);

            // Asked straight out (CompareNotes): the one asked told them.
            var asked = Mill(("rita", "Rita"), ("sam", "Darren"));
            asked.Witness("rita", window, "the man that did the window ran", true, new GameTime(1, 23, 0), 0.9, rung: 2);
            asked.CompareNotes("sam", "rita", new GameTime(2, 9, 0));
            Check(asked.Get("sam").Best("player.window_d1")?.ToldById == "rita", "asked straight out, the one asked is who told them");

            // A look of their own makes it theirs: told by nobody, the heard copy kept beside it.
            mill.Witness("rocco", window, "a man ran past the rank", true, new GameTime(1, 23, 20), 0.7, rung: 1);
            var ronOwn = mill.Get("rocco").Rumors.Where(r => r.TopicKey == "player.window_d1").ToList();
            Check(ronOwn.Exists(r => r.Hops == 0 && r.ToldById == null) && ronOwn.Exists(r => r.Hops == 2 && r.ToldById == "lena"),
                  "once he sees it himself his own look is told by nobody, and what Sheila told him still says so");
            var noRung = Mill(("rita", "Rita"), ("lena", "Sheila"));
            noRung.Witness("rita", new Fact("player", "seen_at", "docks"), "the new owner was down the docks", false, new GameTime(1, 12, 0));
            noRung.Tick(new GameTime(1, 12, 6), (a, b) => true);
            noRung.Witness("lena", new Fact("player", "seen_at", "docks"), "the new owner was down the docks", false, new GameTime(1, 13, 0));
            Check(noRung.Get("lena").Best("player.seen_at").Hops == 0 && noRung.Get("lena").Best("player.seen_at").ToldById == null,
                  "a story heard and then seen for herself is hers, told by nobody");

            // Kept by a save; an older save without it reads as nobody known.
            var json = SaveCodec.Capture(new GameTime(2, 9, 0), new Wallet(10), new Campaign(), new PlayerKnowledge(), new SecretsBook(), new BeatBook(), mill, new DebtBook(), null);
            var again = Mill(("rita", "Rita"), ("lena", "Sheila"), ("rocco", "Ron"));
            SaveCodec.RestoreMillAgents(json, again);
            var olderMill = Mill(("rita", "Rita"), ("lena", "Sheila"), ("rocco", "Ron"));
            SaveCodec.RestoreMillAgents(json.Replace(",\"teller\":\"lena\"", "").Replace(",\"teller\":\"rita\"", ""), olderMill);
            Check(again.Get("rocco").Rumors.Exists(r => r.Hops == 2 && r.ToldById == "lena") && again.Get("rita").Best("player.window_d1").ToldById == null
                  && again.Get("lena").Best("player.window_d1").ToldById == "rita" && json.Contains("\"teller\":\"lena\""),
                  "who told them survives a save");
            Check(!json.Contains("\"teller\":\"rita\""),
                  "a story one telling from the witness saves exactly as before: the witness told it");
            Check(olderMill.Get("rocco").Rumors.TrueForAll(r => r.ToldById == null) && olderMill.Get("lena").Best("player.window_d1").ToldById == "rita",
                  "and a save from before it was kept: one telling out, the witness told them; further out, nobody known");
        }

        static void TestAccountNamesTeller()
        {
            Console.WriteLine("They can say who told them:");
            var mill = Mill(("rita", "Rita"), ("lena", "Sheila"), ("sam", "Darren"));
            mill.Witness("rita", new Fact("player", "window_d1", "seen"), "Nowak put the pawn shop window in", true, new GameTime(1, 23, 0), 0.94, rung: 4);
            mill.Tick(new GameTime(1, 23, 6), (a, b) => true);
            mill.Tick(new GameTime(1, 23, 12), (a, b) => true);
            Func<string, string> nameOf = id => mill.Get(id)?.DisplayName;
            var account = Suspecting.AccountOf(mill.Get("sam"), "player.window_d1", nameOf);
            var derived = Suspecting.Derive(account, new Nearness(), 0.2);
            Check(account.ToldBy == "Sheila" && derived.why.StartsWith("Sheila told me that"),
                  "the second-hand hearer's reason names who told him", derived.why);
            var seen = Suspecting.AccountOf(mill.Get("rita"), "player.window_d1", nameOf);
            Check(seen.ToldBy == null && Suspecting.Derive(seen, new Nearness(), 0.2).why.StartsWith("I saw it myself"),
                  "the one who saw it was told by nobody");
            var unnamed = Suspecting.AccountOf(mill.Get("sam"), "player.window_d1");
            Check(unnamed.ToldBy == null && Suspecting.Derive(unnamed, new Nearness(), 0.2).why.StartsWith("I heard that"),
                  "without names to hand, the reason reads as it always has");
            // The memory of the telling already names the teller; the ladder reads it.
            Check(TalkLadder.HeardFrom("I heard from Sheila that Nowak put the pawn shop window in") == "Sheila"
                  && TalkLadder.HeardFrom("Heard from Rita that the new owner put her window in.") == "Rita"
                  && TalkLadder.HeardFrom("Darren told me, when I asked: Nowak did it") == "Darren"
                  && TalkLadder.HeardFrom("I saw it myself: a man ran") == null,
                  "who told them, read from the memory of the telling");
        }
    }
}
