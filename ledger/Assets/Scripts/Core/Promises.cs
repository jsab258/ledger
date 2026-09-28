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
        public static string SecondDraftNote(IReadOnlyList<string> promised)
        {
            bool silence = false;
            foreach (var p in promised) if (FindSilence(p).Count > 0) silence = true;
            return "- Your first answer promised \"" + string.Join("\"; \"", promised) + "\". You cannot promise to do anything later: " +
                "to meet him, keep watch, lend him anything, pass word on or come round. Nothing in your world would make it happen. " +
                (silence ? "And you will not keep this quiet for him, so never say you will. " : "") +
                "Answer again without promising; if he asks, put him off in your own way.";
        }

        // A PROMISE OF SILENCE (town list 6al): kept only where the Core had
        // them agree to keep the deed quiet, so read everywhere else (the
        // independent check: asked in words the reader missed, "Not a word,
        // Tom." stood and the town's gossip broke it). Said by the speaker of
        // themselves, so advice ("I'd keep that quiet if I were you") and other
        // people ("he'll keep it quiet") are not read as one; and a bare "not a
        // word" only when he spoke of telling (FindSilence's `bareToo`).
        static readonly Regex[] SilenceShapes =
        {
            new Regex(@"\b(i won't|i wont|i will not|i'll not|ill not|i shan't|i shall not|i'll never|i will never|i'd never) (tell|say a word to|breathe a word to|mention it to|let on to) (a soul|a living soul|anyone|anybody|nobody|them|him|her|the police|the law)\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(i won't|i wont|i will not|i'll not|ill not|i shan't) (breathe a word|say a word|say anything|say owt|say nowt|let on|tell a soul)\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(won't|wont|will not|never|nobody'?ll|no one'?ll) hear (it|that|a word|owt) from me\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(i'll|i will|ill|i shall) keep (it|that|this) (quiet|to myself|to meself|under my hat|between us)\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(i'll|i will|ill|i shall) keep (mum|schtum|shtum|quiet|my mouth shut|my trap shut)\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(i'll|i will|ill) say (nothing|nowt)\b(?! (against|bad))", RegexOptions.IgnoreCase),
            new Regex(@"\b(won't|wont|will not|it'll not|that'll not) go any further\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(nobody|no one)'?ll know from me\b", RegexOptions.IgnoreCase),
            new Regex(@"\bmy lips are sealed\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(it|that|this)('ll| will)? (stays?|stay) between us\b", RegexOptions.IgnoreCase),
            new Regex(@"\b(goes|go) no further\b", RegexOptions.IgnoreCase),
            new Regex(@"\byour secret'?s safe\b", RegexOptions.IgnoreCase),
        };
        static readonly Regex[] BareShapes =
        {
            new Regex(@"\bnot a word\b(?! (of|from|since|in|out|more|he|she|they|anyone|anybody|to say))", RegexOptions.IgnoreCase),
            new Regex(@"\bmum's the word\b", RegexOptions.IgnoreCase),
        };

        /// The promises of silence a line makes; empty when none. `bareToo`
        /// reads "not a word" and "mum's the word" as well, for a reply to a line
        /// of his that spoke of telling (Silence.SpeaksOfTelling).
        public static List<string> FindSilence(string text, bool bareToo = true)
        {
            var found = new List<string>();
            if (string.IsNullOrWhiteSpace(text)) return found;
            string t = text.Replace('’', '\'').Replace('‘', '\'');
            foreach (var shape in SilenceShapes)
                foreach (Match m in shape.Matches(t))
                    if (!found.Contains(m.Value)) found.Add(m.Value);
            if (bareToo)
                foreach (var shape in BareShapes)
                    foreach (Match m in shape.Matches(t))
                        if (!found.Contains(m.Value)) found.Add(m.Value);
            return found;
        }
    }
}
