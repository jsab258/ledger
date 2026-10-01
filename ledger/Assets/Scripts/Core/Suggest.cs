using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace Ledger.Core
{
    /// TOM'S SUGGESTED LINES (Jafar, 1 October: "Mixed"; production/design/ui/
    /// STYLE-GUIDE.md, "Suggested lines"; production/research/ui-design/
    /// SUGGESTED-LINES.md): three lines he could say next, in a fixed order of
    /// jobs: one asks about what was just said, one is personal or off the
    /// subject, one leaves. Written by the small model in a call of its own that
    /// is given only what Tom knows (his Ledger and the talk so far), never the
    /// other person's card, memories or secrets, so it cannot point at them.
    /// A line the model gets wrong, and every line when it cannot be asked (no
    /// model, the stand-in, the allowance spent, too slow), comes from his
    /// written lines (production/specs/suggested-lines.json); before anything is
    /// said, the first is a written greeting; a follow-up has no written line, so
    /// without the model's that job is left out (null), as is a job whose written
    /// lines are all spent. Never a line already said or shown
    /// in this conversation; never one that decides a deal (those are written,
    /// from the game's state) or gives his name; never a name Tom has not heard.
    public static class Suggest
    {
        /// About forty letters is the aim; a little over is kept, a paragraph is not.
        public const int MaxLetters = 60;
        public const int Jobs = 3;

        /// His written lines, as production/specs/suggested-lines.json holds them.
        public sealed class Written
        {
            public List<string> Greet = new List<string>(), Leave = new List<string>(), Personal = new List<string>();

            public static Written Parse(string json)
            {
                var w = new Written();
                var doc = MiniJson.AsObject(MiniJson.Deserialize(json));
                if (doc == null) return w;
                List<string> L(string key) => doc.TryGetValue(key, out var v) && MiniJson.AsList(v) is List<object> l
                    ? l.Select(x => x as string).Where(x => !string.IsNullOrWhiteSpace(x)).ToList() : new List<string>();
                w.Greet = L("greet"); w.Leave = L("leave"); w.Personal = L("personal");
                return w;
            }

            /// The written lines for a job: 0 is a greeting before anything is said
            /// and none after (no written follow-up fits after anything, the second
            /// review of 1 October), 1 is personal, 2 leaves.
            public List<string> For(int job, bool started) =>
                job == 0 ? (started ? new List<string>() : Greet) : job == 1 ? Personal : Leave;
        }

        /// The three lines, and which the model wrote (false: a written line).
        public sealed class Result
        {
            public string[] Lines = new string[Jobs];
            public bool[] Generated = new bool[Jobs];
            public string Model;
        }

        /// What the model is told: Tom, the three jobs, and the rules. Nothing of
        /// the person he is talking to but how Tom knows them.
        public const string System =
            "You suggest what Tom Nowak could say next in a conversation. Tom is 32 and the new owner of Mickey's, " +
            "a minicab office on Quay Street in the Hook, an English port town, in 1990; he inherited it from his uncle " +
            "Mickey, who died three weeks before he came. He is a stranger here and never says where he grew up or what " +
            "he did before. Write three things he could say next, in his own plain words: a polite, careful newcomer, " +
            "British English of 1990, never American and never modern. Each is exactly what he says, never a description " +
            "of it, one short sentence of about forty letters. The first asks about what was just said to him. The second " +
            "turns the talk somewhere else, as a newcomer would: something about them, their day or the street, never " +
            "about how he himself is settling in or sleeping. The third ends the conversation politely. Write Mr and Mrs " +
            "without a full stop, and add no times or days that are not below. Use only what is written below: " +
            "never name a person, place, thing or happening that is not in it. Never agree to or refuse anything he is " +
            "being asked, and never give his name. Nothing about drink, pubs, betting or children. Answer with exactly " +
            "three lines starting \"1. \", \"2. \" and \"3. \", and nothing else.";

        /// WHERE THE SECOND LINE MAY TURN (the bench of 1 October: asked alone, the
        /// model put the same idea in nearly every second line, "the flat
        /// upstairs", then "how long have you kept the books"; generated
        /// suggestions converge, the research's warning), one by the turn's seed.
        public static readonly string[] Angles =
        {
            "something about their own day",
            "the street, its shops or its people",
            "how the town has changed",
            "somewhere they would send a newcomer",
            "what they make of something on the street",
            "someone in what Tom knows, if anyone",
            "their work",
        };

        /// The one message the model sees: what Tom knows, the talk so far, and
        /// what he has already been shown.
        public static string Message(IReadOnlyList<string> tomKnows, IReadOnlyList<LlmMessage> heard, string with, IEnumerable<string> shown, int seed = 0)
        {
            var sb = new StringBuilder();
            string them = string.IsNullOrWhiteSpace(with) ? "Them" : with.Trim();
            sb.AppendLine("Who he is talking to, as Tom knows them: " + them + ".");
            sb.AppendLine();
            sb.AppendLine("What Tom knows (his notebook):");
            var known = (tomKnows ?? Array.Empty<string>()).Where(k => !string.IsNullOrWhiteSpace(k)).ToList();
            if (known.Count == 0) sb.AppendLine("- nothing written down yet");
            foreach (var k in known) sb.AppendLine("- " + k.Trim());
            sb.AppendLine();
            sb.AppendLine("The conversation so far:");
            var said = (heard ?? Array.Empty<LlmMessage>()).Where(m => m != null && !string.IsNullOrWhiteSpace(m.Content)).ToList();
            if (said.Count == 0) sb.AppendLine("(nothing yet: he has just walked up)");
            foreach (var m in said) sb.AppendLine((m.Role == "user" ? "Tom" : them) + ": " + m.Content.Trim());
            var before = (shown ?? Array.Empty<string>()).Where(s => !string.IsNullOrWhiteSpace(s)).ToList();
            if (before.Count > 0)
            {
                sb.AppendLine();
                sb.AppendLine("Already suggested in this conversation (never again):");
                foreach (var s in before) sb.AppendLine("- " + s.Trim());
            }
            sb.AppendLine();
            sb.AppendLine("For the second, turn to " + Angles[(int)((uint)seed % (uint)Angles.Length)] + ". Never ask what they have already told him.");
            return sb.ToString();
        }

        static readonly Regex Numbered = new Regex(@"^\s*([123])[.)]\s*(.+?)\s*$");

        /// The model's three lines by job, or null where it gave none.
        public static string[] Parse(string text)
        {
            var lines = new string[Jobs];
            foreach (var raw in (text ?? "").Split('\n'))
            {
                var m = Numbered.Match(raw);
                if (!m.Success) continue;
                int job = m.Groups[1].Value[0] - '1';
                if (lines[job] != null) continue;
                lines[job] = m.Groups[2].Value.Trim().Trim('"', '“', '”').Trim();
            }
            return lines;
        }

        static string Norm(string s) => Regex.Replace((s ?? "").ToLowerInvariant().Replace('’', '\''), @"[^a-z0-9' ]", "").Trim();

        static readonly Regex Capitalised = new Regex(@"\b[A-Z][a-z']+\b");
        static readonly Regex TimeWord = new Regex(@"\b(this morning|this afternoon|this evening|tonight|today|yesterday|tomorrow|this week|last week|next week|this weekend|at the weekend|these days)\b", RegexOptions.IgnoreCase);
        static readonly HashSet<string> AlwaysHis = new HashSet<string> { "I", "I'm", "I'll", "I've", "I'd", "Tom", "Mickey", "Mickey's", "Mr", "Mrs", "Miss" };

        /// Why a model's line may not be offered, or null when it may.
        public static string Refuse(string line, string context, ISet<string> spent)
        {
            if (string.IsNullOrWhiteSpace(line)) return "empty";
            if (line.Length > MaxLetters) return "too long";
            if (line.Contains('\n') || line.Contains(':')) return "not a line he says";
            if (spent.Contains(Norm(line))) return "already said or shown";
            if (ContentRule.SpeechBreaks(line) != null) return "the content rule";
            if (RealWorld.Find(line).Count > 0) return "a real name or a later thing";
            if (Arrangement.ConfirmsNo(line) || Arrangement.SoundsLikeNo(line)) return "decides Ron's ask";
            if (WeeksEnd.Sounds(line) != WeekAnswer.None
                || WeeksEnd.Confirms(line, WeekAnswer.WindDown) || WeeksEnd.Confirms(line, WeekAnswer.TakeOver) || WeeksEnd.Confirms(line, WeekAnswer.WontSay))
                return "answers Sheila's question";
            if (PlayerIdentity.GivesName(line).gave) return "gives his name";
            // A time it cannot know (the bench of 1 October: "this morning", "this
            // week"): the call is not told the hour, so only one it was told.
            var when = TimeWord.Match(line);
            if (when.Success && context.IndexOf(when.Value, StringComparison.OrdinalIgnoreCase) < 0) return "a time it was not told: " + when.Value;
            // A name Tom has not heard: a capitalised word, after the first, that is
            // in nothing he knows or has heard.
            var words = Capitalised.Matches(line).Cast<Match>().ToList();
            foreach (var w in words)
            {
                bool sentenceStart = w.Index == 0 || Regex.IsMatch(line.Substring(0, w.Index), @"[.!?]\s*$");
                if (sentenceStart || AlwaysHis.Contains(w.Value)) continue;
                if (context.IndexOf(w.Value, StringComparison.Ordinal) < 0) return "a name he has not heard: " + w.Value;
            }
            return null;
        }

        /// The written line for a job, never one already said or shown: the first
        /// fresh one from the seed, or none when all are spent (never twice).
        public static string WrittenFor(Written w, int job, bool started, ISet<string> spent, int seed)
        {
            var lines = (w ?? new Written()).For(job, started);
            if (lines.Count == 0) return null;
            int start = (int)((uint)seed % (uint)lines.Count);
            for (int i = 0; i < lines.Count; i++)
            {
                var l = lines[(start + i) % lines.Count];
                if (!spent.Contains(Norm(l))) return l;
            }
            return null;
        }

        /// The three lines. `llm` null (the stand-in, or no model) gives the written
        /// ones; so does a model that fails, is refused or is too slow.
        public static async Task<Result> WriteAsync(ILlmClient llm, Written written, IReadOnlyList<string> tomKnows,
            IReadOnlyList<LlmMessage> heard, string with, ICollection<string> shown, int seed,
            CostTracker cost = null, TimeSpan? timeout = null, string model = Models.Ambient, CancellationToken ct = default)
        {
            var result = new Result();
            bool started = heard != null && heard.Any(m => m != null && !string.IsNullOrWhiteSpace(m.Content));
            var spent = new HashSet<string>((shown ?? new List<string>()).Select(Norm));
            foreach (var m in heard ?? Array.Empty<LlmMessage>())
                if (m != null && m.Role == "user") spent.Add(Norm(m.Content));
            string[] wrote = new string[Jobs];
            if (llm != null)
            {
                var message = Message(tomKnows, heard, with, shown, seed);
                try
                {
                    using var cts = CancellationTokenSource.CreateLinkedTokenSource(ct);
                    cts.CancelAfter(timeout ?? TimeSpan.FromSeconds(6));
                    var req = new LlmRequest { Model = model, System = System, MaxTokens = 160 };
                    req.Messages.Add(new LlmMessage("user", message));
                    var resp = await llm.CompleteAsync(req, cts.Token);
                    cost?.Record(resp.Model ?? model, resp.InputTokens, resp.OutputTokens);
                    wrote = Parse(resp.Text);
                    result.Model = string.IsNullOrEmpty(resp.Model) ? model : resp.Model;
                    // What a name may come from: what he knows and has heard.
                    var context = message;
                    for (int job = 0; job < Jobs; job++)
                    {
                        // Before anything is said, the first is a written greeting.
                        if (job == 0 && !started) { wrote[job] = null; continue; }
                        if (wrote[job] != null && Refuse(wrote[job], context, spent) != null) wrote[job] = null;
                        if (wrote[job] != null) spent.Add(Norm(wrote[job]));
                    }
                }
                // Any failure (too slow, refused by the allowance, no answer) gives the
                // written lines: a suggestion is never worth an error.
                catch (Exception)
                {
                    wrote = new string[Jobs];
                }
            }
            for (int job = 0; job < Jobs; job++)
            {
                if (wrote[job] != null) { result.Lines[job] = wrote[job]; result.Generated[job] = true; continue; }
                var w = WrittenFor(written, job, started, spent, seed + job * 7);
                result.Lines[job] = w;
                if (w != null) spent.Add(Norm(w));
            }
            if (!result.Generated.Any(g => g)) result.Model = null;
            return result;
        }
    }
}
