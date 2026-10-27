using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Ledger.Core
{
    /// THE FAST CHECKER (his page pick of 27 October 2026, night: the third try's small checker at the open cut-off, in
    /// the game behind a switch, measured live before it is on by default). A first sentence it scores under its cut-off
    /// is said without waiting for Haiku's check; anything else, or no answer in time, goes to Haiku as before. The hard
    /// rule on names runs before it (ConversationEngine), so no named stranger is ever cleared by it.
    ///
    /// It talks to tools/checkers/checker_server.py, the checker exactly as measured, in a process of its own; its
    /// settings live in production/specs/fast-checker.json. A request it does not answer within the spec's time counts
    /// as no answer: the sentence waits for Haiku, never for it.
    public sealed class FastChecker : IDisposable
    {
        readonly Process _proc;
        readonly System.Collections.Concurrent.ConcurrentDictionary<int, TaskCompletionSource<double?>> _waiting =
            new System.Collections.Concurrent.ConcurrentDictionary<int, TaskCompletionSource<double?>>();
        readonly object _write = new object();
        int _id;
        public double Cut { get; }
        public string CutName { get; }
        public int AnswerWithinMs { get; }
        /// What the last scored sentence got, and how long it took (for the record).
        public double? LastScore { get; private set; }
        public long LastMs { get; private set; }

        FastChecker(Process proc, double cut, string cutName, int within)
        {
            _proc = proc; Cut = cut; CutName = cutName; AnswerWithinMs = within;
            // ONE READER for the server's answers, each handed to the request waiting under its id; one that came too
            // late finds nobody waiting and is dropped.
            Task.Run(async () =>
            {
                try
                {
                    string line;
                    while ((line = await _proc.StandardOutput.ReadLineAsync().ConfigureAwait(false)) != null)
                    {
                        var r = MiniJson.AsObject(MiniJson.Deserialize(line));
                        if (r == null || !r.TryGetValue("id", out var rid) || rid == null) continue;
                        int id = Convert.ToInt32(rid, System.Globalization.CultureInfo.InvariantCulture);
                        if (!_waiting.TryRemove(id, out var tcs)) continue;
                        tcs.TrySetResult(r.TryGetValue("score", out var sc) && sc != null
                            ? Convert.ToDouble(sc, System.Globalization.CultureInfo.InvariantCulture) : (double?)null);
                    }
                }
                catch (Exception) { }
                foreach (var kv in _waiting) kv.Value.TrySetResult(null);
            });
        }

        /// Starts the server from the spec and waits for its ready line; null, with why, when it cannot.
        public static FastChecker Start(string specPath, string serverScript, out string why, int readyWithinMs = 120000)
        {
            why = null;
            try
            {
                var spec = MiniJson.AsObject(MiniJson.Deserialize(File.ReadAllText(specPath)));
                string python = spec["python"] as string;
                double cut = Convert.ToDouble(spec["cut"], System.Globalization.CultureInfo.InvariantCulture);
                string cutName = spec.TryGetValue("cutName", out var cn) ? cn as string : null;
                int within = spec.TryGetValue("answerWithinMs", out var w) ? Convert.ToInt32(w, System.Globalization.CultureInfo.InvariantCulture) : 400;
                if (!File.Exists(python)) { why = "no python at " + python; return null; }
                if (!File.Exists(serverScript)) { why = "no server at " + serverScript; return null; }
                var psi = new ProcessStartInfo(python, "-I \"" + serverScript + "\" \"" + specPath + "\"")
                {
                    UseShellExecute = false, RedirectStandardInput = true, RedirectStandardOutput = true, RedirectStandardError = true,
                    CreateNoWindow = true, StandardOutputEncoding = Encoding.UTF8,
                };
                var proc = Process.Start(psi);
                proc.ErrorDataReceived += (s, e) => { };
                proc.BeginErrorReadLine();
                var ready = proc.StandardOutput.ReadLineAsync();
                if (!ready.Wait(readyWithinMs) || ready.Result == null || ready.Result.IndexOf("\"ready\": true", StringComparison.Ordinal) < 0)
                {
                    why = "the server never said it was ready";
                    try { proc.Kill(); } catch (Exception) { }
                    return null;
                }
                return new FastChecker(proc, cut, cutName, within);
            }
            catch (Exception e) { why = e.GetType().Name + ": " + e.Message; return null; }
        }

        /// The sentence's score, or null when the server did not answer in time or could not score it.
        public async Task<double?> ScoreAsync(IEnumerable<(string id, string text)> known, string probe, string sentence, CancellationToken ct)
        {
            var sw = Stopwatch.StartNew();
            int id = Interlocked.Increment(ref _id);
            var tcs = new TaskCompletionSource<double?>(TaskCreationOptions.RunContinuationsAsynchronously);
            _waiting[id] = tcs;
            try
            {
                var lines = new List<object>();
                foreach (var (kid, text) in known) lines.Add(kid + ": " + text);
                var req = new Dictionary<string, object> { { "id", id }, { "known", lines }, { "probe", probe ?? "" }, { "detail", sentence } };
                lock (_write)
                {
                    _proc.StandardInput.WriteLine(MiniJson.Serialize(req));
                    _proc.StandardInput.Flush();
                }
                var done = await Task.WhenAny(tcs.Task, Task.Delay(AnswerWithinMs, ct)).ConfigureAwait(false);
                if (done != tcs.Task) return null;
                var score = tcs.Task.Result;
                if (score.HasValue) { LastScore = score; LastMs = sw.ElapsedMilliseconds; }
                return score;
            }
            catch (Exception) when (!ct.IsCancellationRequested) { return null; }
            finally { _waiting.TryRemove(id, out _); }
        }

        public void Dispose()
        {
            try { _proc.StandardInput.Close(); } catch (Exception) { }
            try { if (!_proc.WaitForExit(2000)) _proc.Kill(); } catch (Exception) { }
            _proc.Dispose();
        }
    }
}
