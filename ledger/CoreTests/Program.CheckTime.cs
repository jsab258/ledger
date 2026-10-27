using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

namespace Ledger.CoreTests
{
    /// THE CHECK'S OWN TIME (his speech order, 27 October: the check is the lever left). Each change to how fast the
    /// check runs gets its checks here; none may change what it lets through.
    static partial class Program
    {
        /// A checker that writes its list in two parts, a pause apart, and answers each second look after a while,
        /// noting when each look was asked for and whether the list was still being written then.
        class StreamedList : IStreamingLlmClient
        {
            readonly string _first, _rest;
            readonly Func<string, bool> _supported;
            public TimeSpan Pause = TimeSpan.FromMilliseconds(400), LookTime = TimeSpan.FromMilliseconds(200);
            /// The stream that breaks after its first part, as a dropped connection does.
            public bool Break;
            public int Streams, PlainLists, LooksCancelled;
            public volatile bool ListDone;
            public readonly List<(string detail, bool whileWritten)> Looks = new List<(string, bool)>();
            public StreamedList(string first, string rest, Func<string, bool> supported) { _first = first; _rest = rest; _supported = supported; }

            static bool IsList(LlmRequest r) => r.System.StartsWith("You read one line", StringComparison.Ordinal);

            public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default)
            {
                if (!IsList(request)) return await CompleteAsync(request, ct);
                Streams++;
                onText(_first);
                await Task.Delay(Pause, ct);
                if (Break) throw new LlmStreamBrokenException("the connection dropped mid-reply");
                onText(_first + _rest);
                ListDone = true;
                return new LlmResponse { Text = _first + _rest, StopReason = "end_turn", InputTokens = 10, OutputTokens = 10, Model = request.Model };
            }

            public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
            {
                if (IsList(request))
                {
                    PlainLists++;
                    await Task.Delay(Pause, ct);
                    ListDone = true;
                    return new LlmResponse { Text = _first + _rest, StopReason = "end_turn", InputTokens = 10, OutputTokens = 10, Model = request.Model };
                }
                var content = request.Messages[0].Content;
                int at = content.IndexOf("1. ", StringComparison.Ordinal);
                string detail = at < 0 ? "" : content.Substring(at + 3).Split('\n')[0].Trim();
                lock (Looks) Looks.Add((detail, !ListDone));
                try { await Task.Delay(LookTime, ct); }
                catch (OperationCanceledException) { Interlocked.Increment(ref LooksCancelled); throw; }
                string verdict = _supported(detail) ? "{\"verdicts\": [{\"n\": 1, \"supported\": true, \"source\": \"M1\"}]}"
                                                    : "{\"verdicts\": [{\"n\": 1, \"supported\": false}]}";
                return new LlmResponse { Text = verdict, StopReason = "end_turn", InputTokens = 10, OutputTokens = 10, Model = request.Model };
            }
        }

        /// THE SECOND LOOKS STARTED AS THE LIST IS WRITTEN (ClaimCheck.EarlyLooks): the same requests and the same
        /// verdict as the finished list's, the looks only asked for sooner.
        static void TestEarlyLooks()
        {
            Console.WriteLine("The second looks started as the list is written (ClaimCheck.EarlyLooks):");
            var card = CharacterCard.Parse("# Ron Kirby\nid: rocco\ntier: core\n\n## Summary\nA docker until 1989, now on Mickey's door. He keeps the rank.\n" +
                "## Speech Style\nSays things like 'saw a van on the rank'.\n## Hard Facts\n- Mickey kept him on.\n");
            var mems = new List<MemoryEvent> { new MemoryEvent(new GameTime(1, 12, 0), "heard", 0.9, "Heard the man that did the window ran off through the yard.") };
            var items = ClaimCheck.KnownItems(card, mems, new string[0], "he was seen near it", "The yard, evening.", new GameTime(1, 14, 0).ToString());
            string hard = items.First(i => i.text.Contains("Mickey kept him on")).id;
            string mem = items.First(i => i.text.Contains("ran off through the yard")).id;
            // The van flagged and written first; then a memory's detail (supported at the list) and the card's own words
            // (stated word for word, cleared by code): neither ever needs a look.
            string first = "{\"specifics\": [{\"detail\": \"a white van\", \"kind\": \"vehicle\", \"source\": \"none\"}, ";
            string rest = "{\"detail\": \"ran off through the yard\", \"kind\": \"action\", \"source\": \"" + mem + "\"}, " +
                          "{\"detail\": \"Mickey kept him on\", \"kind\": \"person\", \"source\": \"" + hard + "\"}]}";
            const string line = "A white van, he ran off through the yard. Mickey kept him on.";
            bool was = ClaimCheck.EarlyLooks;
            try
            {
                ClaimCheck.EarlyLooks = false;
                var off = new StreamedList(first, rest, d => false);
                var swOff = Stopwatch.StartNew();
                var a = ClaimCheck.CheckAsync(off, "m", items, line, CancellationToken.None).GetAwaiter().GetResult();
                swOff.Stop();
                Check(off.Streams == 0 && off.PlainLists == 1, "off, the list is asked for in one piece, as before");

                ClaimCheck.EarlyLooks = true;
                var on = new StreamedList(first, rest, d => false);
                var swOn = Stopwatch.StartNew();
                var b = ClaimCheck.CheckAsync(on, "m", items, line, CancellationToken.None).GetAwaiter().GetResult();
                swOn.Stop();
                Check(on.Streams == 1 && on.PlainLists == 0, "on, the list is streamed");
                Check(on.Looks.Count == 1 && on.Looks[0].detail == "a white van" && on.Looks[0].whileWritten,
                      "the flagged van's look is asked for while the list is still being written",
                      string.Join(" / ", on.Looks.Select(l => l.detail + (l.whileWritten ? " (early)" : " (after)"))));
                Check(off.Looks.Count == 1 && !off.Looks[0].whileWritten, "off, it is asked for only once the list is done");
                Check(a.invented != null && b.invented != null && a.invented.SequenceEqual(b.invented) && b.invented.SequenceEqual(new[] { "a white van" }),
                      "the verdict is the same either way: only the van refused",
                      $"off [{string.Join(", ", a.invented ?? new List<string>())}] on [{string.Join(", ", b.invented ?? new List<string>())}]");
                Check(a.calls.Count == 2 && b.calls.Count == 2, "and it costs the same calls: the list and one look",
                      $"off {a.calls.Count}, on {b.calls.Count}");
                Console.WriteLine($"  (timed: off {swOff.ElapsedMilliseconds} ms, on {swOn.ElapsedMilliseconds} ms; the list 400 ms, a look 200 ms)");

                var cleared = new StreamedList(first, rest, d => d == "a white van");
                var c = ClaimCheck.CheckAsync(cleared, "m", items, line, CancellationToken.None).GetAwaiter().GetResult();
                Check(c.invented != null && c.invented.Count == 0 && c.calls.Count == 2, "an early look that supports the van clears it, as a late one does");

                // A broken stream: asked again in one piece, and the look already started is the one used.
                var broken = new StreamedList(first, rest, d => false) { Break = true };
                var e = ClaimCheck.CheckAsync(broken, "m", items, line, CancellationToken.None).GetAwaiter().GetResult();
                Check(broken.PlainLists == 1 && broken.Looks.Count == 1 && e.invented != null && e.invented.SequenceEqual(new[] { "a white van" }) && e.calls.Count == 2,
                      "a stream that breaks is asked for again whole; the early look is used, not asked twice",
                      $"plain lists {broken.PlainLists}, looks {broken.Looks.Count}, calls {e.calls.Count}");

                // More than MaxLooks flagged: the list's verdict stands with no looks, and those started early are
                // stopped rather than waited for.
                var many = Enumerable.Range(1, ClaimCheck.MaxLooks + 1).Select(i => "{\"detail\": \"van number " + i + "\", \"kind\": \"vehicle\", \"source\": \"none\"}").ToList();
                string manyFirst = "{\"specifics\": [" + string.Join(", ", many.Take(5)) + ", ";
                string manyRest = string.Join(", ", many.Skip(5)) + "]}";
                var wholesale = new StreamedList(manyFirst, manyRest, d => true) { LookTime = TimeSpan.FromMilliseconds(3000) };
                var swMany = Stopwatch.StartNew();
                var m = ClaimCheck.CheckAsync(wholesale, "m", items, "Vans.", CancellationToken.None).GetAwaiter().GetResult();
                swMany.Stop();
                Check(m.invented != null && m.invented.Count == ClaimCheck.MaxLooks + 1 && m.calls.Count == 1,
                      "a line made up wholesale keeps the list's verdict, the list's call alone counted",
                      $"{m.invented?.Count} refused, {m.calls.Count} calls");
                Check(wholesale.Looks.Count == 5 && swMany.ElapsedMilliseconds < 2500,
                      "the looks started early for it are stopped, not waited for",
                      $"{wholesale.Looks.Count} started, back in {swMany.ElapsedMilliseconds} ms");
                SpinWait.SpinUntil(() => Volatile.Read(ref wholesale.LooksCancelled) == 5, 2000);
                Check(Volatile.Read(ref wholesale.LooksCancelled) == 5, "and each is cancelled", $"{wholesale.LooksCancelled} cancelled");

                // A client that cannot stream: the switch changes nothing.
                var plain = new ScriptedLlm("{\"specifics\": [{\"detail\": \"a van\", \"kind\": \"vehicle\", \"source\": \"none\"}]}",
                                            "{\"verdicts\": [{\"n\": 1, \"supported\": false}]}");
                var p = ClaimCheck.CheckAsync(plain, "m", items, "A van.", CancellationToken.None).GetAwaiter().GetResult();
                Check(p.invented != null && p.invented.Count == 1 && p.calls.Count == 2 && plain.Requests.Count == 2,
                      "with a client that cannot stream, the check runs as before");
            }
            finally { ClaimCheck.EarlyLooks = was; }
        }

        /// A checker whose every call's copies are scripted in turn: when the model begins each (its thinking
        /// included), when its first words come, when it ends, and what it says; a copy may fail before it begins, or
        /// break after its first words. Stopped copies are noted.
        class ScriptedCopies : IStartingLlmClient
        {
            public readonly Queue<(int begin, int first, int end, string text, bool fail, bool breakAfterFirst, bool breakBeforeBegin)> Copies =
                new Queue<(int, int, int, string, bool, bool, bool)>();
            public int Streams, Plain, Stopped;
            public string PlainText = "{\"specifics\": []}";
            public void Add(int begin, int first, int end, string text, bool fail = false, bool breakAfterFirst = false, bool breakBeforeBegin = false) =>
                Copies.Enqueue((begin, first, end, text, fail, breakAfterFirst, breakBeforeBegin));
            public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
            {
                Plain++;
                return Task.FromResult(new LlmResponse { Text = PlainText, StopReason = "end_turn", InputTokens = 10, OutputTokens = 10, Model = request.Model });
            }
            public Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default) =>
                StreamAsync(request, onText, null, ct);
            public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, Action onStart, CancellationToken ct = default)
            {
                (int begin, int first, int end, string text, bool fail, bool breakAfterFirst, bool breakBeforeBegin) c;
                lock (Copies) { c = Copies.Dequeue(); Streams++; }
                try
                {
                    await Task.Delay(c.begin, ct);
                    if (c.fail) throw new LlmApiException(529, "overloaded");
                    if (c.breakBeforeBegin) throw new LlmStreamBrokenException("an error sent mid-stream");
                    onStart?.Invoke();
                    await Task.Delay(Math.Max(0, c.first - c.begin), ct);
                    onText?.Invoke(c.text.Substring(0, Math.Max(1, c.text.Length / 3)));
                    await Task.Delay(Math.Max(0, c.end - c.first), ct);
                    if (c.breakAfterFirst) throw new LlmStreamBrokenException("the connection dropped mid-reply");
                    onText?.Invoke(c.text);
                    return new LlmResponse { Text = c.text, StopReason = "end_turn", InputTokens = 10, OutputTokens = 10, Model = request.Model };
                }
                catch (OperationCanceledException) when (ct.IsCancellationRequested)
                {
                    Interlocked.Increment(ref Stopped);
                    throw new LlmStreamStoppedException(new LlmResponse { InputTokens = 10, OutputTokens = 1, Model = request.Model }, ct);
                }
            }
        }

        /// TWO COPIES OF EACH CHECK CALL, THE ONE BEGUN FIRST KEPT (ClaimCheck.TwoCopies): kept by when the model began
        /// it, never by its first words or by which ends first, so neither a refusal's longer answer nor a look's
        /// longer thinking can lose the race to a pass.
        static void TestTwoCopies()
        {
            Console.WriteLine("Two copies of each check call, the one begun first kept (ClaimCheck.TwoCopies):");
            var card = CharacterCard.Parse("# Ron Kirby\nid: rocco\ntier: core\n\n## Summary\nA docker until 1989, now on Mickey's door.\n" +
                "## Speech Style\nPlain.\n## Hard Facts\n- Mickey kept him on.\n");
            var items = ClaimCheck.KnownItems(card, new List<MemoryEvent>(), new string[0], "he was seen near it", "The yard, evening.", new GameTime(1, 14, 0).ToString());
            const string refuse = "{\"specifics\": [{\"detail\": \"a white van\", \"kind\": \"vehicle\", \"source\": \"none\"}]}";
            const string pass = "{\"specifics\": []}";
            const string notSupported = "{\"verdicts\": [{\"n\": 1, \"supported\": false}]}";
            const string supported = "{\"verdicts\": [{\"n\": 1, \"supported\": true, \"source\": \"H1\"}]}";
            bool was = ClaimCheck.TwoCopies;
            try
            {
                ClaimCheck.TwoCopies = true;
                // The list: copy one begun first, its first words last and its end last (a refusal's longer answer);
                // copy two ends first (a pass). The look: copy one begun first but thinking longer (its verdict, not
                // supported, written after copy two's supported one).
                var c = new ScriptedCopies();
                c.Add(30, 300, 400, refuse);
                c.Add(100, 150, 200, pass);
                c.Add(20, 300, 350, notSupported);
                c.Add(80, 120, 160, supported);
                var a = ClaimCheck.CheckAsync(c, "m", items, "A white van.", CancellationToken.None).GetAwaiter().GetResult();
                Check(a.invented != null && a.invented.SequenceEqual(new[] { "a white van" }),
                      "the copy the model began first is kept, though the other wrote first and ended first: the list's refusal and the look's stand",
                      a.invented == null ? "unknown" : "[" + string.Join(", ", a.invented) + "]");
                Check(c.Streams == 4 && c.Stopped == 2, "each call went out twice, and each copy begun later was stopped",
                      $"{c.Streams} sent, {c.Stopped} stopped");
                Check(a.calls.Count == 2 && a.calls[0].InputTokens == 20 && a.calls[1].InputTokens == 20,
                      "each call counts once, its stopped copy's tokens added to the kept answer's, for the cost",
                      string.Join(", ", a.calls.Select(x => x.InputTokens)));

                // A copy that fails before it begins leaves the other to answer.
                var f = new ScriptedCopies();
                f.Add(10, 10, 10, pass, fail: true);
                f.Add(80, 100, 120, pass);
                var b = ClaimCheck.CheckAsync(f, "m", items, "Evening.", CancellationToken.None).GetAwaiter().GetResult();
                Check(b.invented != null && b.invented.Count == 0 && f.Plain == 0, "a copy that fails leaves the other to answer");

                // Both refused outright fails the call as one copy refused does.
                var both = new ScriptedCopies();
                both.Add(10, 10, 10, pass, fail: true);
                both.Add(20, 20, 20, pass, fail: true);
                bool threw = false;
                try { ClaimCheck.CheckAsync(both, "m", items, "Evening.", CancellationToken.None).GetAwaiter().GetResult(); }
                catch (LlmApiException) { threw = true; }
                Check(threw && both.Plain == 0, "both copies refused outright fail the call, as one copy refused does");

                // Both breaking before the model began either (the fresh review: an error sent mid-stream threw with no
                // retry, where the plain call has three): asked again whole.
                var bothBroke = new ScriptedCopies { PlainText = pass };
                bothBroke.Add(20, 30, 60, refuse, breakBeforeBegin: true);
                bothBroke.Add(30, 40, 60, refuse, breakBeforeBegin: true);
                var g = ClaimCheck.CheckAsync(bothBroke, "m", items, "Evening.", CancellationToken.None).GetAwaiter().GetResult();
                Check(bothBroke.Plain == 1 && g.invented != null && g.invented.Count == 0,
                      "both copies breaking before either began: the call is asked for again whole, as the plain call retries a drop",
                      $"plain {bothBroke.Plain}");

                // The kept copy breaking after its first words, the other already stopped: asked again in one piece.
                var broke = new ScriptedCopies { PlainText = refuse };
                broke.Add(20, 40, 100, refuse, breakAfterFirst: true);
                broke.Add(200, 220, 250, pass);
                broke.Add(20, 40, 60, notSupported);
                broke.Add(200, 220, 250, notSupported);
                var d = ClaimCheck.CheckAsync(broke, "m", items, "A white van.", CancellationToken.None).GetAwaiter().GetResult();
                Check(broke.Plain == 1 && d.invented != null && d.invented.SequenceEqual(new[] { "a white van" }),
                      "the kept copy breaking after its first words is asked for again whole",
                      $"plain {broke.Plain}, [{string.Join(", ", d.invented ?? new List<string>())}]");

                // A client that cannot say when the model begins makes its one plain call: no race on first words.
                var noStart = new StreamedList("{\"specifics\": [], ", "\"x\": 1}", _ => false);
                var h = ClaimCheck.CheckAsync(noStart, "m", items, "Evening.", CancellationToken.None).GetAwaiter().GetResult();
                Check(noStart.Streams == 0 && noStart.PlainLists == 1 && h.invented != null,
                      "a client that cannot say when the model begins gets one plain call, never a race on first words");

                // Off: one copy, the plain call, as before.
                ClaimCheck.TwoCopies = false;
                var off = new ScriptedCopies { PlainText = pass };
                var e = ClaimCheck.CheckAsync(off, "m", items, "Evening.", CancellationToken.None).GetAwaiter().GetResult();
                Check(off.Streams == 0 && off.Plain == 1 && e.invented != null && e.invented.Count == 0, "off, each call goes out once, as before");
            }
            finally { ClaimCheck.TwoCopies = was; }

            // THE BUDGET SETTLES A STOPPED STREAM AT WHAT IT USED (the fresh review: its worst case stayed counted).
            var inner = new ScriptedCopies();
            inner.Add(2000, 2100, 2200, pass);
            var capped = new BudgetedClient(inner, 1.0);
            var stop = new CancellationTokenSource();
            var req = new LlmRequest { Model = "claude-haiku-5-5", MaxTokens = 4300 };
            req.Messages.Add(new LlmMessage("user", "hello"));
            var call = capped.StreamAsync(req, null, null, stop.Token);
            double reservedAt = capped.SpentUsd;
            stop.Cancel();
            bool stoppedThrew = false;
            try { call.GetAwaiter().GetResult(); } catch (LlmStreamStoppedException) { stoppedThrew = true; }
            double settled = capped.SpentUsd;
            double used = 10 / 1_000_000.0 * 0.10 + 1 / 1_000_000.0 * 0.50;
            Check(stoppedThrew && reservedAt > 0.001 && Math.Abs(settled - used) < 1e-9,
                  "a stream stopped on purpose is settled at what it used, not left at its worst case",
                  $"reserved US${reservedAt:0.000000}, settled US${settled:0.000000}, used US${used:0.000000}");

            // Stopped before the service answered at all (the cancellation arrives as a plain one, with no use to
            // read): settled at its prompt, counted as read, nothing written; never left at its worst case.
            var early = new BudgetedClient(new NeverAnswers(), 1.0);
            var stopEarly = new CancellationTokenSource();
            var callEarly = early.StreamAsync(req, null, null, stopEarly.Token);
            stopEarly.Cancel();
            bool earlyThrew = false;
            try { callEarly.GetAwaiter().GetResult(); } catch (OperationCanceledException) { earlyThrew = true; }
            double prompt = (5 / 4.0 * 1.1 + 50) / 1_000_000.0 * 0.10;
            Check(earlyThrew && early.SpentUsd < reservedAt / 10 && early.SpentUsd > 0,
                  "a stream stopped before any answer is settled at its prompt, not its worst case",
                  $"settled US${early.SpentUsd:0.000000} (its prompt US${prompt:0.000000}), worst case US${reservedAt:0.000000}");
        }

        /// A service that never answers: its stream waits until it is cancelled, and the cancellation is all it says.
        class NeverAnswers : IStartingLlmClient
        {
            public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default) => throw new InvalidOperationException("not used");
            public Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default) => StreamAsync(request, onText, null, ct);
            public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, Action onStart, CancellationToken ct = default)
            {
                await Task.Delay(TimeSpan.FromSeconds(30), ct);
                return null;
            }
        }
    }
}
