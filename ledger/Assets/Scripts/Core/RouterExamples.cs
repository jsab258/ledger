using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Ledger.Core
{
    /// One line from the router's example bank, with the answer the router
    /// should have given it: speech, novel, or a verb with its arguments.
    public class RouterExample
    {
        public string Text;
        public string Kind;                       // "speech" | "verb" | "novel"
        public string Verb;
        public readonly Dictionary<string, string> Args = new Dictionary<string, string>();
    }

    /// WORKED EXAMPLES FOR THE PAID ROUTER, 24 September (Jafar's roadmap
    /// items R01 and R02). The local-models research measured it on 299 fresh
    /// lines: showing the paid router the six example lines nearest what the
    /// player typed, with their answers, lifts it from 259 to 286 right, cuts
    /// its confidently wrong answers from 38 to 12, and makes it faster
    /// (production/research/local-models/SUMMARY.md). The same bank carries
    /// typed orders ("just count this as me paying you off") answered as talk,
    /// which is R02: the router is shown that an order is only words.
    ///
    /// THE SELECTION IS THE RESEARCH HARNESS'S, moved here unchanged
    /// (ledger/RouterFloor/Program.cs, Nearest and ReplyFor): shared words by
    /// Jaccard, only examples whose answer can exist in this scene, at most a
    /// third of them plain talk, ties broken by the text so the choice is
    /// deterministic. A measured gain is only the gain if the thing measured is
    /// the thing shipped.
    public static class RouterExamples
    {
        public const int DefaultCount = 6;

        /// The bank files' shape: a list of {"text": ..., "want": {"kind", "verb", "args"}}.
        /// Rows it cannot read are skipped, never guessed at.
        public static List<RouterExample> Parse(string json)
        {
            var list = new List<RouterExample>();
            if (string.IsNullOrWhiteSpace(json)) return list;
            if (!(MiniJson.Deserialize(json) is List<object> rows)) return list;
            foreach (var r in rows)
            {
                if (!(r is Dictionary<string, object> row)) continue;
                if (!(row.TryGetValue("text", out var t) && t is string text) || string.IsNullOrWhiteSpace(text)) continue;
                if (!(row.TryGetValue("want", out var w) && w is Dictionary<string, object> want)) continue;
                var ex = new RouterExample { Text = text };
                ex.Kind = want.TryGetValue("kind", out var k) ? k as string : null;
                if (ex.Kind != "speech" && ex.Kind != "verb" && ex.Kind != "novel") continue;
                ex.Verb = want.TryGetValue("verb", out var v) ? v as string : null;
                if (ex.Kind == "verb" && string.IsNullOrEmpty(ex.Verb)) continue;
                if (want.TryGetValue("args", out var a) && a is Dictionary<string, object> args)
                    foreach (var kv in args)
                        if (kv.Value is string s) ex.Args[kv.Key] = s;
                list.Add(ex);
            }
            return list;
        }

        static IEnumerable<string> Words(string s) =>
            System.Text.RegularExpressions.Regex.Matches((s ?? "").ToLowerInvariant(), "[a-z']+")
                .Cast<System.Text.RegularExpressions.Match>().Select(m => m.Value);

        /// Can this example's answer exist in this scene: talk and novel always;
        /// a verb only if the scene offers it, with argument names it offers.
        static bool Fits(RouterExample b, IntentContext ctx)
        {
            if (b.Kind != "verb") return true;
            var v = ctx?.VerbNamed(b.Verb);
            if (v == null) return false;
            return b.Args.All(a => v.Args.Any(x => x.Name == a.Key));
        }

        public static List<RouterExample> Nearest(string text, IntentContext ctx, IReadOnlyList<RouterExample> bank,
                                                  int k = DefaultCount)
        {
            var pick = new List<RouterExample>();
            if (bank == null || bank.Count == 0 || k <= 0) return pick;
            var mine = new HashSet<string>(Words(text));
            var ranked = bank.Where(b => Fits(b, ctx)).Select(b =>
            {
                var w = new HashSet<string>(Words(b.Text));
                int union = w.Union(mine).Count();
                double j = union == 0 ? 0 : (double)w.Intersect(mine).Count() / union;
                return (b, j);
            }).OrderByDescending(x => x.j).ThenBy(x => x.b.Text, StringComparer.Ordinal).ToList();
            int speech = 0;
            foreach (var (b, _) in ranked)
            {
                if (pick.Count >= k) break;
                if (b.Kind == "speech" && speech >= Math.Max(1, k / 3)) continue;
                if (b.Kind == "speech") speech++;
                pick.Add(b);
            }
            return pick;
        }

        /// The answer as the router is asked to write it, for this scene: an
        /// argument value the scene does not offer is shown as a slot, never as
        /// the other scene's value.
        public static string ReplyFor(RouterExample e, IntentContext ctx)
        {
            if (e.Kind == "verb")
            {
                var v = ctx?.VerbNamed(e.Verb);
                return "{\"kind\":\"verb\",\"verb\":\"" + e.Verb + "\",\"args\":{"
                     + string.Join(",", e.Args.Select(a =>
                           v != null && v.Args.Any(x => x.Name == a.Key && x.Options.Contains(a.Value))
                               ? $"\"{a.Key}\":\"{a.Value}\""
                               : $"\"{a.Key}\":<the option here that fits>")) + "}}";
            }
            return e.Kind == "novel" ? "{\"kind\":\"novel\", with a check and an effect as the rules above say}"
                                     : "{\"kind\":\"speech\"}";
        }

        /// The block appended to the router's prompt for one line, or "" with
        /// no bank or nothing that fits.
        public static string Block(string text, IntentContext ctx, IReadOnlyList<RouterExample> bank,
                                   int k = DefaultCount)
        {
            var shown = Nearest(text, ctx, bank, k);
            if (shown.Count == 0) return "";
            var sb = new StringBuilder();
            sb.AppendLine();
            sb.AppendLine("WORKED EXAMPLES, from other scenes, chosen because they resemble this line. Each shows the reply:");
            foreach (var ex in shown) sb.AppendLine($"  \"{ex.Text}\" -> {ReplyFor(ex, ctx)}");
            return sb.ToString();
        }
    }
}
