using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

namespace Ledger.CoreTests
{
    /// THE FASTER FIRST SENTENCE, ITS SECOND TRY (his order of 28 October 2026, D12;
    /// production/research/live-speech-architecture/FAST-GROUNDED-TALK-2026-10-28.md): the bench's switches on
    /// ConversationEngine, and the two faults the fresh review found in the 7 October code.
    static partial class Program
    {
        /// A model that writes `fast` for the faster model's first sentence, `rest` when told the reply has begun, and
        /// `whole` for any other draft, each streamed a sentence and a bit first; the check finds nothing.
        class SplitFake : IStreamingLlmClient
        {
            readonly string _fastModel, _fast, _rest, _whole;
            public readonly List<LlmRequest> Asked = new List<LlmRequest>();
            public bool FastStopped;
            public SplitFake(string fastModel, string fast, string rest, string whole) { _fastModel = fastModel; _fast = fast; _rest = rest; _whole = whole; }
            static bool IsCheck(LlmRequest r) => r.System != null && (r.System.StartsWith("You read one line") || r.System.StartsWith("You check details"));
            public bool IsFast(LlmRequest r) => r.Model == _fastModel && r.MaxTokens == ConversationEngine.FirstMaxTokens;
            public static bool IsRest(LlmRequest r) => r.System != null && r.System.Contains("YOUR REPLY HAS ALREADY BEGUN");

            public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
            {
                lock (Asked) Asked.Add(request);
                var text = IsCheck(request) ? (request.System.StartsWith("You check details") ? "{\"verdicts\":[]}" : "{\"specifics\":[]}") : _whole;
                return Task.FromResult(new LlmResponse { Text = text, StopReason = "end_turn", InputTokens = 100, OutputTokens = 10, Model = request.Model });
            }

            public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default)
            {
                if (IsCheck(request)) { var r = await CompleteAsync(request, ct); onText(r.Text); return r; }
                lock (Asked) Asked.Add(request);
                bool fast = IsFast(request);
                var text = fast ? _fast : IsRest(request) ? _rest : _whole;
                int cut = text.IndexOf(". ", StringComparison.Ordinal);
                if (cut > 0)
                {
                    onText(text.Substring(0, cut + 3));
                    try { await Task.Delay(60, ct); }
                    catch (OperationCanceledException)
                    {
                        if (fast) FastStopped = true;
                        throw new LlmStreamStoppedException(new LlmResponse { Text = text.Substring(0, cut + 3), InputTokens = 100, OutputTokens = 5, Model = request.Model }, ct);
                    }
                }
                if (text.Length > 0) onText(text);
                return new LlmResponse { Text = text, StopReason = "end_turn", InputTokens = 100, OutputTokens = 10, Model = request.Model };
            }
        }

        static async Task TestFastFirstSplit()
        {
            Console.WriteLine("The faster first sentence, second try:");
            var now = new GameTime(1, 12, 0);
            string wasFirst = ConversationEngine.FirstModel, wasOver = ConversationEngine.FirstModelOnlyOver;
            bool wasStrict = ConversationEngine.StrictGoOn, wasThink = ConversationEngine.ReplyThinkingOff;
            async Task<(string reply, List<string> handed, SplitFake llm, ConversationEngine engine)> Turn(string model, string fast, string rest, string whole)
            {
                var llm = new SplitFake("claude-haiku-5-5", fast, rest, whole);
                var engine = new ConversationEngine(llm, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker())
                { Checker = llm, Model = model };
                var handed = new List<string>();
                var reply = await engine.SayToAsync("Who are you?", now, "In the office.", default, s => { lock (handed) handed.Add(s); return Task.FromResult(true); });
                return (reply, handed, llm, engine);
            }
            try
            {
                Check(ConversationEngine.AcceptsThinkingOff("claude-sonnet-5") && ConversationEngine.AcceptsThinkingOff("claude-haiku-5-5")
                      && ConversationEngine.AcceptsThinkingOff("claude-haiku-4-5") && !ConversationEngine.AcceptsThinkingOff("claude-sonnet-5-5")
                      && !ConversationEngine.AcceptsThinkingOff(null),
                    "thinking is turned off only on models that accept it (Sonnet 5 and the Haikus; Sonnet 5.5 refuses it)");
                Check(ConversationEngine.EndedSentence("Aye, I keep the books.") == "Aye, I keep the books." && ConversationEngine.EndedSentence("Aye. Books.") == null
                      && ConversationEngine.EndedSentence("Aye, I keep") == null && ConversationEngine.EndedSentence("  ") == null
                      && ConversationEngine.EndedSentence("Mr. Kirby keeps the door.") == "Mr. Kirby keeps the door.",
                    "an ended reply is one first sentence only when it is exactly one whole sentence");

                // THE SPLIT, AS ARM B RUNS IT: Haiku 5.5 thinking off, the stricter note, the rest held short.
                ConversationEngine.FirstModel = "claude-haiku-5-5";
                ConversationEngine.FirstModelOnlyOver = Models.Core;
                ConversationEngine.StrictGoOn = true;
                ConversationEngine.ReplyThinkingOff = true;
                var b = await Turn(Models.Core, "I keep the books here. And more besides.", "The office is upstairs.", "I keep the books here. The office is upstairs.");
                var fastReq = b.llm.Asked.FirstOrDefault(b.llm.IsFast);
                var restReq = b.llm.Asked.FirstOrDefault(SplitFake.IsRest);
                Check(fastReq != null && fastReq.Thinking == "disabled" && b.llm.FastStopped,
                    "the faster model writes the first sentence with its thinking off, stopped there");
                Check(restReq != null && restReq.System.Contains("Most replies end there") && restReq.System.Contains("\"I keep the books here.\"")
                      && restReq.MaxTokens == ConversationEngine.RestMaxTokens && restReq.Thinking == "disabled" && restReq.Model == Models.Core,
                    "the turn's own model writes the rest under the stricter note, held short, thinking off",
                    restReq == null ? "no rest asked" : restReq.MaxTokens + " " + restReq.Thinking);
                Check(b.reply == "I keep the books here. The office is upstairs." && b.handed.Count == 1 && b.handed[0] == "I keep the books here."
                      && b.engine.LastFirstFast && b.engine.LastFirstSentence == "I keep the books here.",
                    "the first sentence is handed over, the reply is the two together, and the engine says who wrote the first", b.reply);

                // ONLY OVER THE CONVERSATION'S MODEL: small talk on another model is never split.
                var small = await Turn(Models.Ambient, "I keep the books here. And more.", "Upstairs.", "Mm. Quiet one.");
                Check(!small.llm.Asked.Any(small.llm.IsFast) && !small.llm.Asked.Any(SplitFake.IsRest) && !small.engine.LastFirstFast,
                    "small talk on another model is never split, whatever the faster model is");

                // A FAST SENTENCE THAT WOULD BE HELD BACK is not the reply's start: the turn's own model writes it all.
                var held = await Turn(Models.Core, "Right, that's me off " + ConversationEngine.DoneMark + ". See you.", "Nothing.", "I keep the books here. The office is upstairs.");
                Check(!held.llm.Asked.Any(SplitFake.IsRest) && held.reply == "I keep the books here. The office is upstairs." && !held.engine.LastFirstFast
                      && held.engine.LastSteps.Any(s => s.step == "first-fast-held"),
                    "a faster first sentence that would be held back is dropped, and the turn's own model writes the whole reply", held.reply);

                // A FASTER REPLY OF ONE WHOLE SENTENCE is the first sentence when its stream ends.
                var one = await Turn(Models.Core, "Aye, I keep the books.", "", "I keep the books here. The office is upstairs.");
                Check(one.handed.Count == 1 && one.handed[0] == "Aye, I keep the books." && one.llm.Asked.Any(SplitFake.IsRest) && one.reply == "Aye, I keep the books."
                      && one.engine.LastFirstFast,
                    "a faster reply of one whole sentence is handed over, and a rest of nothing leaves it alone", one.reply + " / " + string.Join("|", one.handed));

                // ARM A0: one model, thinking off; ARM A, today's: no thinking field at all.
                ConversationEngine.FirstModel = null;
                ConversationEngine.FirstModelOnlyOver = null;
                ConversationEngine.StrictGoOn = false;
                var a0 = await Turn(Models.Core, "", "", "I keep the books here. The office is upstairs.");
                Check(a0.llm.Asked.Where(r => r.MaxTokens == 300).All(r => r.Thinking == "disabled") && a0.llm.Asked.Any(r => r.MaxTokens == 300),
                    "with the reply's thinking off, every draft on Sonnet 5 is sent thinking disabled");
                var a55 = await Turn("claude-sonnet-5-5", "", "", "I keep the books here. The office is upstairs.");
                Check(a55.llm.Asked.Where(r => r.MaxTokens == 300).All(r => r.Thinking == null), "and never on a model that refuses it");
                ConversationEngine.ReplyThinkingOff = false;
                var a = await Turn(Models.Core, "", "", "I keep the books here. The office is upstairs.");
                Check(a.llm.Asked.Where(r => r.MaxTokens == 300).All(r => r.Thinking == null) && !a.engine.LastFirstFast && a.engine.LastFirstSentence == "I keep the books here.",
                    "off, as the game ships, a draft sends no thinking field, and the turn's own model writes the first sentence");
                Check(!ConversationEngine.GoOnNote("Aye.").Contains("Most replies end there"), "and the note of 7 October stands while the stricter one is off");
            }
            finally
            {
                ConversationEngine.FirstModel = wasFirst;
                ConversationEngine.FirstModelOnlyOver = wasOver;
                ConversationEngine.StrictGoOn = wasStrict;
                ConversationEngine.ReplyThinkingOff = wasThink;
            }
        }
    }
}
