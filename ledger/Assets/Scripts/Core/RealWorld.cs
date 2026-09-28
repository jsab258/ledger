using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// REAL NAMES AND LATER THINGS IN LIVE TALK (town list 6ao; V4 against
    /// canon's "Brands and law", the third checklist sweep). Canon: every brand,
    /// band, club, product and vehicle is fictional, no real people or car
    /// models; the era is 1988 to 1992. Friends will make small talk ("what are
    /// you smoking?", "who do you support?", "nice car, what is it?"), and a
    /// model reaches for the real cigarette, club or maker. The project's brand
    /// and era lists (tools/canon-gate.py) govern only authored files, and read
    /// as they are they would refuse ordinary speech ("courage", "players",
    /// "shell"), so this list is the speech-safe part: names nobody says for
    /// anything else, and the capitalised ones only where written as a name.
    /// A reply that uses one is asked again without it, as a promise is.
    public static class RealWorld
    {
        // Said in any case: nobody means anything else by them.
        static readonly string[] AnyCase =
        {
            // cars and makers
            "vauxhall", "cortina", "datsun", "toyota", "volvo", "volkswagen", "peugeot", "renault", "skoda", "lada",
            "mercedes", "bmw", "austin allegro", "morris minor", "austin maestro", "ford escort", "ford sierra", "ford capri", "ford transit",
            // tobacco
            "marlboro", "rothmans", "silk cut", "benson and hedges", "benson & hedges", "lambert and butler", "woodbines", "superkings", "dunhill", "john player",
            // food, drink and shops
            "coca-cola", "coca cola", "pepsi", "tizer", "irn-bru", "irn bru", "lucozade", "cadbury", "kit kat", "kitkat", "hovis", "bovril", "pg tips", "typhoo",
            "nescafe", "nescafé", "heinz", "woolworths", "woolies", "marks and spencer", "marks & spencer", "marks and sparks", "tesco", "sainsbury",
            "kwik save", "asda", "dixons", "rumbelows", "currys", "whsmith", "wh smith",
            // television, radio and papers
            "coronation street", "eastenders", "emmerdale", "brookside", "blind date", "top of the pops", "only fools and horses", "news at ten",
            "match of the day", "the bbc", "itv", "channel 4", "channel four", "radio 1", "radio one", "radio 2", "radio two", "sky tv",
            "daily mail", "daily mirror", "daily express", "daily star", "news of the world",
            // football clubs that are not also a town's name
            "manchester united", "man united", "man utd", "tottenham hotspur", "leeds united", "newcastle united",
            "west ham", "aston villa", "nottingham forest", "sheffield wednesday",
            // public figures
            "thatcher", "kinnock", "john major", "princess diana", "prince charles", "gazza", "gascoigne", "kylie", "jason donovan",
            "bobby robson", "scargill", "gorbachev", "mandela", "saddam",
            // later than 1992
            "mobile phone", "mobile", "cell phone", "cellphone", "smartphone", "internet", "website", "email", "e-mail", "wifi", "wi-fi",
            "texted", "text message", "social media", "selfie", "google", "iphone", "facebook", "twitter", "netflix", "dvd", "laptop",
        };
        // Written as a name only (a capital, mid-sentence): "a Ford", "the Sun".
        static readonly string[] AsName =
        {
            "Ford", "Rover", "Jag", "Jaguar", "Transit", "Mini", "Escort", "Sierra", "Capri", "Rolls",
            "Embassy", "Regal", "Players", "Celtic", "Rangers", "Everton", "Spurs", "Arsenal", "BBC", "ITV", "Sun", "Mirror", "Guardian", "Telegraph",
            "Boots", "Heineken", "Queen",
        };

        static readonly Regex AnyCaseRx = Build(AnyCase, RegexOptions.IgnoreCase);
        static readonly Regex AsNameRx = Build(AsName, RegexOptions.None);

        static Regex Build(string[] names, RegexOptions options)
        {
            var parts = new List<string>();
            foreach (var n in names) parts.Add(Regex.Escape(n));
            parts.Sort((a, b) => b.Length.CompareTo(a.Length));
            return new Regex(@"(?<![\w'])(" + string.Join("|", parts) + @")(?![\w-])", options);
        }

        /// The real names and later things a line says; empty when none. A
        /// capitalised name at the start of a sentence is not read ("Rover's
        /// barking" would still be; "Transit" opening a sentence is too rare to
        /// guess at), nor "mobile" as in "mobile library".
        public static List<string> Find(string text)
        {
            var found = new List<string>();
            if (string.IsNullOrWhiteSpace(text)) return found;
            string t = text.Replace('’', '\'');
            foreach (Match m in AnyCaseRx.Matches(t))
            {
                string v = m.Value;
                if (v.ToLowerInvariant() == "mobile" && Regex.IsMatch(t.Substring(m.Index), @"^mobile (library|home|shop|van|crane|unit)", RegexOptions.IgnoreCase)) continue;
                if (!found.Contains(v)) found.Add(v);
            }
            foreach (Match m in AsNameRx.Matches(t))
            {
                // Not at the start of the line or of a sentence.
                int i = m.Index - 1;
                while (i >= 0 && (t[i] == ' ' || t[i] == '"' || t[i] == '\'')) i--;
                if (i < 0 || t[i] == '.' || t[i] == '!' || t[i] == '?') continue;
                if (!found.Contains(m.Value)) found.Add(m.Value);
            }
            return found;
        }

        /// The prompt's rule, in the content rule's shape (ConversationEngine;
        /// here, beside the list, so the era's words live in the one file the
        /// canon gate knows names them in order to refuse them).
        public const string PromptRule = "- Your world has its own makes, brands, shops, clubs, papers and programmes, and none of them is a real one: never name a real make of car, cigarette, drink or food, a shop, a football club, a newspaper, a television or radio programme or channel, a band or singer, or any real public figure. Say it the way people do without the name: \"an old estate\", \"my usual\", \"the match\", \"the telly\", \"the paper\". It is 1990: nobody has a mobile phone, the internet or email; there is the phone box, a letter, the paper.";

        /// The note that asks for a second draft without them.
        public static string SecondDraftNote(IReadOnlyList<string> named) =>
            "- Your first answer named \"" + string.Join("\"; \"", named) + "\". Nothing in your world is called that: no real make, brand, shop, " +
            "club, paper, programme or famous person exists there, and nobody has a mobile phone, the internet or email. " +
            "Answer again saying it the way people do without the name.";
    }
}
