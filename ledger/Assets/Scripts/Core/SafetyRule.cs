using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// WHAT NO CHARACTER MAY SAY TO A PLAYER, apart from canon (town list 6e,
    /// 28 September). Canon's content rule (ContentRule, D17 and D18) says what
    /// the world holds; this says what a live model may never say to the person
    /// playing: urging them to harm or kill themselves. Steam asks what stops
    /// live AI saying what it must not, and every comparable game names
    /// self-harm among the things it blocks (production/research/runtime-ai-business/notes/stores.md, 1d).
    ///
    /// NARROW ON PURPOSE, as the content gate is: threats and violence are the
    /// genre and stay ("I'll kill you", "I'll cut your throat", "he's better off
    /// dead"), and so does the everyday British idiom the independent check
    /// listed: "you'll kill yourself lifting that crate", "don't kill yourself
    /// rushing", "you take your life in your hands crossing Quay Street", "take
    /// the night off yourself", "go and hang yourself a coat up", "mind you don't
    /// hurt yourself". Only the second person urged towards their own death or
    /// harm is caught.
    public static class SafetyRule
    {
        const RegexOptions O = RegexOptions.IgnoreCase | RegexOptions.Compiled;

        // Not after "don't", "you'll", "you'd" (a warning, not an urging), and not
        // before a verb in -ing ("kill yourself lifting that") or an object
        // ("hang yourself a coat up").
        const string NotWarned = @"(?<!\b(?:don't|dont|do\s+not|you'll|you\s+will|you'd|you\s+would|won't|or\s+you'll)\s+(?:\w+\s+)?)";
        const string NotIdiom = @"(?!\s+(?:\w+ing\b|a\b|an\b|some\b|in\s+(?:paperwork|work|debt)\b))";

        static readonly (string id, Regex pattern)[] Rules =
        {
            ("self-harm/urge", new Regex(NotWarned + @"\b(?:kill|top|hang|drown)\s+yourself\b" + NotIdiom + "|" +
                                          NotWarned + @"\bdo\s+yourself\s+in\b" + NotIdiom, O)),
            ("self-harm/throw", new Regex(@"\bthrow\s+yourself\s+(?:off|under|in\s+front\s+of|into)\b|" +
                                           @"\bjump\s+off\s+(?:the|a|that)\s+(?:bridge|quay|roof|building|cliff|pier|jetty)\b", O)),
            ("self-harm/life", new Regex(@"\b(?:end|take)\s+your\s+(?:own\s+)?life\b(?!\s+in\s+your\s+hands)|" +
                                          @"\b(?:you\s+(?:should|could|might\s+as\s+well|ought\s+to)|go\s+(?:and|on,?)|why\s+(?:don't|not)(?:\s+you)?)(?:\s+just)?\s+end\s+it\s+all\b", O)),
            ("self-harm/thought", new Regex(@"\b(?:thought\s+(?:about|of)|considered|think\s+(?:about|of))\s+(?:killing|topping|hanging|drowning)\s+yourself\b", O)),
            ("self-harm/method", new Regex(@"\b(?:slit|cut|open)\s+your\s+(?:own\s+)?(?:wrists?|veins?)\b", O)),
            ("self-harm/worth", new Regex(@"\byou(?:'d|\s+would|'re|\s+are)?\s+(?:be\s+)?better\s+off\s+dead\b|" +
                                           @"\b(?:nobody|no\s*one|no-one)(?:'d|\s+would|'ll|\s+will)?\s+miss\s+you\b", O)),
        };

        /// Which rule a line breaks, as "kind/id", or null when it breaks none.
        /// Curly apostrophes are read as straight ones, whatever path the line
        /// came by (the independent check: "you’d be better off dead" passed
        /// where nothing had straightened it).
        public static string SpeechBreaks(string text)
        {
            if (string.IsNullOrWhiteSpace(text)) return null;
            text = text.Replace('’', '\'').Replace('‘', '\'');
            foreach (var (id, pattern) in Rules)
                if (pattern.IsMatch(text)) return id;
            return null;
        }
    }
}
