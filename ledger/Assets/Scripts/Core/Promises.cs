using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// A PROMISE THE WORLD WILL NOT KEEP (town list 6af, the second checklist
    /// sweep, A31.07): friends will try "keep an eye out for me tonight", "meet
    /// me at the quay at nine", "lend us a tenner". A character who agrees and
    /// then does nothing is the invented person again, a promise the world
    /// cannot keep; the claim check reads what happened, not what somebody says
    /// they will do.
    ///
    /// NARROW ON PURPOSE. Only the plain shapes of a commitment to do something
    /// later for the player: meeting him somewhere, keeping watch, lending him
    /// something, passing word, coming round. "I'll tell you what", "see you
    /// later" and "I'll give you that" are how people talk, and a redraft over
    /// them would cost a second draft for nothing.
    public static class Promises
    {
        static readonly Regex[] Shapes =
        {
            // meeting him somewhere, at some time
            new Regex(@"\b(meet|see) you (at|by|outside|down at|round at|in|on|over at|up at)\b(?! (all|last))", RegexOptions.IgnoreCase),
            new Regex(@"\b(meet|see) you (there|tonight|tomorrow)\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(i'll|i will|ill) meet you\b", RegexOptions.IgnoreCase),
            // keeping watch for him
            new Regex(@"\b(i'll|i will|ill) (keep|have) (an eye|a look ?out|watch)\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(i'll|i will|ill) (watch|mind) (the|your|it|that|him|her|them)\b", RegexOptions.IgnoreCase),
            // lending or giving him something
            new Regex(@"\b(i'll|i will|ill) (lend|loan|sub) you\b", RegexOptions.IgnoreCase),
            // passing word, asking round
            new Regex(@"\b(i'll|i will|ill) (let you know|ask around|ask about|ask round|put the word out|pass it on|pass the word|have a word)\b", RegexOptions.IgnoreCase),
            new Regex(@"\bleave it with me\b", RegexOptions.IgnoreCase),
            // coming to him
            new Regex(@"\b(i'll|i will|ill) (come|be) (round|by|over|there)\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(i'll|i will|ill) (sort it|get it|fetch it) for you\b", RegexOptions.IgnoreCase),
        };

        /// The promises a line makes, as the words that make them; empty when none.
        public static List<string> Find(string text)
        {
            var found = new List<string>();
            if (string.IsNullOrWhiteSpace(text)) return found;
            string t = text.Replace('’', '\'').Replace('‘', '\'');
            foreach (var shape in Shapes)
                foreach (Match m in shape.Matches(t))
                    if (!found.Contains(m.Value)) found.Add(m.Value);
            return found;
        }

        /// The note that asks for a second draft without the promise.
        public static string SecondDraftNote(IReadOnlyList<string> promised) =>
            "- Your first answer promised \"" + string.Join("\"; \"", promised) + "\". You cannot promise to do anything later: " +
            "to meet him, keep watch, lend him anything, pass word on or come round. Nothing in your world would make it happen. " +
            "Answer again without promising; if he asks, put him off in your own way.";
    }
}
