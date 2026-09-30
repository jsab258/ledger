using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// A SENTENCE WITH NOTHING IN IT TO CHECK (town list T1, 29 September): made
    /// only of the plain words people fill talk with ("Mm.", "Fair.", "Couldn't
    /// tell you, friend."), no name, number, time, place, thing, count or deed,
    /// and nothing said of anyone but the speaker and the listener ("He was
    /// there.", "My son would know." and "Just the one." are claims: the
    /// independent check); how they address him only as address. It can state
    /// nothing the simulation does not know, so a reply's first sentence that is
    /// plain is spoken without waiting for its own check. Measured on the claim
    /// bench's 480 labelled replies: 44 first sentences (9%) are plain, and of
    /// the 227 replies that invented something, none had the invention in one.
    public static class PlainWords
    {
        static readonly HashSet<string> Plain = new HashSet<string>((
            "mm hm hmm mhm well right aye yes yeah yep no nope nah oh ah eh now then listen alright okay ok sorry thanks ta please " +
            "i you it we me us my your its our mine yours this that these those " +
            "what who where when why how which whatever " +
            "am is are be do does will would can could shall should may might must " +
            "know think say tell ask mean want need like hear sure suppose reckon expect wonder mind care matter " +
            "not never just only very quite much more less so too enough really maybe perhaps still even all any something anything nothing everything " +
            "a an the of to about for with as " +
            "and but or if because than " +
            "good bad fine fair true wrong funny odd daft " +
            "dont doesnt cant couldnt wont wouldnt isnt arent shouldnt mustnt " +
            "im id ill youre youve youd youll thats whats whos weve " +
            // A REACTION BEFORE THE ANSWER (the builder's delay note, step 5, 30
            // September): the words a moment's reaction is made of, none of which
            // can carry a person, place, time, thing or deed on its own.
            "depends asking wants knows question honest honestly blimey cor ooh dunno heck gosh crikey wait er erm um let thinking").Split(' '));

        // The same, as phrases only: "on" and "course" alone can carry a claim
        // ("It's on.", "a course"), "Hang on." and "Of course." cannot.
        static readonly Regex PlainPhrases = new Regex(@"\b(hang|hold|go|come) on\b|\bof course\b", RegexOptions.IgnoreCase);

        // HOW THEY ADDRESS HIM, only as address: after a comma at the end ("Right
        // you are, boss.") or before one at the start ("Boss, I couldn't say.").
        // Anywhere else a person ("My son would know.", "Boss.": the independent
        // check, and the bench's own check flagged "Boss").
        static readonly Regex AddressAtEnd = new Regex(@",\s*(boss|friend|mate|love|son|dear|sir|pet|lad|lass|pal)\s*([.!?]+)?\s*$", RegexOptions.IgnoreCase);
        static readonly Regex AddressAtStart = new Regex(@"^\s*(boss|friend|mate|love|son|dear|sir|pet|lad|lass|pal)\s*,", RegexOptions.IgnoreCase);

        static List<string> Words(string s)
        {
            var w = new List<string>();
            foreach (Match m in Regex.Matches((s ?? "").ToLowerInvariant().Replace('’', '\'').Replace("'", ""), "[a-z]+")) w.Add(m.Value);
            return w;
        }

        /// Whether the sentence is plain: words only from the plain list, no digit.
        public static bool IsPlain(string sentence)
        {
            if (string.IsNullOrWhiteSpace(sentence) || Regex.IsMatch(sentence, "[0-9]")) return false;
            var bare = AddressAtStart.Replace(AddressAtEnd.Replace(sentence, "$2"), "");
            var w = Words(PlainPhrases.Replace(bare, " "));
            // Nothing left but a plain phrase ("Of course.") is plain; nothing at all ("Boss.") is not.
            if (w.Count == 0) return PlainPhrases.IsMatch(bare);
            foreach (var x in w) if (!Plain.Contains(x)) return false;
            return true;
        }
    }
}
