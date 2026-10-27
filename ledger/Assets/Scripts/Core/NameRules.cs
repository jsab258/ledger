using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// THE HARD RULE ON NAMES (his order of 27 October 2026, evening, 3): "no sentence that names a person, place or
    /// event missing from the speaker's facts may pass, whether through the fast checker or Haiku." ClaimCheck runs it
    /// before any call: a name missing refuses the sentence there and then. Code, not a model, so nothing talks it
    /// round. The reference and its measurements are tools/checkers/name_rule.py (designed on the tuning half; on the
    /// 617 held sentences it refused no true sentence, and stopped none of the 35 inventions Haiku lets through,
    /// which describe rather than name: "the harbourmaster", "half past seven").
    ///
    /// A name is a run of capitalised words, a possessive taken off ("Mickey's" is Mickey), titles kept in the run
    /// but never enough alone (Father Walsh is Walsh). A sentence's first word starts a name only when the next word
    /// is capitalised too ("Frank Doyle ..."): alone it is the capital every sentence opens with, so a lone invented
    /// name opening a sentence ("Frank was in") is not caught. Days, months and holidays are times, numbers numbers,
    /// nationalities and oaths not people, "I" the speaker. A name is in the facts when any of its words other than a
    /// title or a common word ("The Crown" is judged on Crown) is a word of the facts, in any case.
    ///
    /// Wider (off; measured apart, for his word): also every number the sentence states (a clock time, a count, a
    /// year) must be a number the facts state, and a place or a role named by a plain noun from a short list (the
    /// pier, the chemist's, the harbourmaster) a word of the facts. On the 617 it stopped 7 of the 35, all harmful,
    /// and refused no true sentence.
    public static class NameRules
    {
        static readonly HashSet<string> Titles = new HashSet<string>
        {
            "father", "mr", "mrs", "miss", "ms", "dr", "doctor", "saint", "st", "old", "young", "uncle", "aunt", "auntie",
            "sister", "brother", "mother", "nurse", "officer", "constable", "pc", "ds", "sergeant", "inspector", "detective",
        };
        static readonly HashSet<string> Times = new HashSet<string>
        {
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "january", "february", "march",
            "april", "may", "july", "august", "september", "october", "november", "december", "christmas", "easter",
            "whitsun", "boxing", "new", "year", "eve", "bank", "holiday",
        };
        static readonly HashSet<string> Nations = new HashSet<string>
        {
            "english", "british", "irish", "scottish", "scots", "welsh", "geordie", "geordies", "northern", "southern",
            "yorkshire", "lancashire",
        };
        static readonly HashSet<string> Oaths = new HashSet<string> { "god", "christ", "lord", "heaven", "heavens", "jesus", "hell" };
        static readonly HashSet<string> Common = new HashSet<string>(("a about after again ah all also always an and any anyone anything are as " +
            "ask at aye away back be because been before being best better between bit both but by can can't come could couldn't course did " +
            "didn't do does doesn't done don't down each either else enough even ever every everyone everything exactly fair far few fine " +
            "first for from get give go goes going gone good got had has hasn't have haven't he he'd he'll he's her here here's hers him his " +
            "honest how however i if in is isn't it it'll it's its just keep kind know last least leave less let let's like listen little " +
            "look lot love mate maybe me mind mine more most much must my myself near need never next no nobody none nor not nothing now " +
            "of off oh ok okay on once one only or other our ours out over pal perhaps plenty pretty quite rather really right round same " +
            "say see seems she she'd she'll she's should since so some somebody someone something sometimes sorry still such sure take tell " +
            "than thank thanks that that'll that's the their them then there there's these they they'd they'll they're they've thing things " +
            "think this those though three through till to today told tomorrow tonight too two under until up upstairs downstairs us very " +
            "wait want was wasn't way we we'd we'll we're we've well were weren't what what's whatever when where where's whether which while " +
            "who who's whoever whole why will with without won't would wouldn't yeah yes yet you you'd you'll you're you've your yours four " +
            "five six seven eight nine ten twenty half quarter word nah son love lad lass pet hen chief boss sir madam funny strange odd " +
            "straight head truth work depends aside apart morning afternoon evening night cheers ta blimey honestly frankly hardly mostly " +
            "usually second third find turn walk follow try").Split(' '));
        static readonly string[] Units = { "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
                                           "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen" };
        static readonly string[] Tens = { "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety" };
        static readonly Regex NumberWord = new Regex(@"^(one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|" +
                                                     @"fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|" +
                                                     @"eighty|ninety|hundred|thousand)(-[a-z]+)?$");
        static readonly HashSet<string> PlaceNouns = new HashSet<string>
        {
            "pier", "chemist", "chemists", "pub", "inn", "church", "school", "station", "harbour", "hospital", "library", "post", "bank",
            "garage", "mill", "factory", "warehouse", "club", "hotel", "cinema", "park", "shop", "shops", "bakery", "butcher", "butchers",
            "awning", "allotments", "flats", "estate", "beach", "promenade", "lighthouse", "bus", "ferry", "landing", "market", "cafe",
            "laundry", "launderette", "chapel", "yard", "docks", "quay",
        };
        static readonly HashSet<string> RoleNouns = new HashSet<string>
        {
            "harbourmaster", "landlord", "landlady", "vicar", "priest", "doctor", "police", "constable", "dispatcher", "foreman",
            "manager", "cleaner", "barman", "postman", "milkman", "councillor", "solicitor",
        };
        static readonly Regex Word = new Regex(@"[A-Za-z][A-Za-z'’\-]*");
        static readonly Regex SentenceEnd = new Regex(@"(?<=[.!?])\s+");
        static readonly Regex OneAsPronoun = new Regex(@"\b(the|that|this|any|no|every|which) one\b|\bone of\b|\bone another\b|\bone day\b");

        static string Norm(string w)
        {
            w = w.Replace('’', '\'');
            foreach (var s in new[] { "'s", "s'", "'" })
                if (w.ToLowerInvariant().EndsWith(s) && w.Length > s.Length + 1) return w.Substring(0, w.Length - s.Length);
            return w;
        }

        static bool Capitalised(string w)
        {
            string low = w.ToLowerInvariant();
            return w.Length > 0 && char.IsUpper(w[0]) && w != "I" && !low.StartsWith("i'") && !Nations.Contains(low) && !Oaths.Contains(low)
                   && !Times.Contains(low) && !Times.Contains(low.TrimEnd('s')) && !NumberWord.IsMatch(low);
        }

        /// The names a line states, each a run of words.
        public static List<List<string>> Names(string line)
        {
            var outRuns = new List<List<string>>();
            foreach (var sentence in SentenceEnd.Split((line ?? "").Trim()))
            {
                var toks = Word.Matches(sentence).Cast<Match>().Select(m => Norm(m.Value)).ToList();
                var run = new List<string>();
                for (int i = 0; i < toks.Count; i++)
                {
                    bool isName = Capitalised(toks[i]);
                    if (isName && i == 0 && !(toks.Count > 1 && Capitalised(toks[1]))) isName = false;
                    if (isName) { run.Add(toks[i]); continue; }
                    if (run.Count > 0) outRuns.Add(run);
                    run = new List<string>();
                }
                if (run.Count > 0) outRuns.Add(run);
            }
            return outRuns;
        }

        static HashSet<string> FactWords(IEnumerable<string> facts) =>
            new HashSet<string>(Word.Matches(string.Join(" ", facts)).Cast<Match>().Select(m => Norm(m.Value).ToLowerInvariant()));

        /// The numbers a text states: digits, number words (a year read as its last two digits too).
        public static HashSet<int> Numbers(string text)
        {
            var nums = new HashSet<int>();
            string low = (text ?? "").ToLowerInvariant().Replace('’', '\'');
            foreach (Match d in Regex.Matches(low, @"\d+"))
                if (int.TryParse(d.Value, out int n)) { nums.Add(n); if (n >= 1900) nums.Add(n % 100); }
            var words = Regex.Matches(low, "[a-z]+").Cast<Match>().Select(m => m.Value).ToList();
            for (int i = 0; i < words.Count; i++)
            {
                int t = System.Array.IndexOf(Tens, words[i]);
                int u = System.Array.IndexOf(Units, words[i]);
                if (t >= 0)
                {
                    int next = i + 1 < words.Count ? System.Array.IndexOf(Units, words[i + 1]) : -1;
                    nums.Add(20 + 10 * t + (next >= 0 && next < 9 ? next + 1 : 0));
                }
                else if (u >= 0 && !(i > 0 && System.Array.IndexOf(Tens, words[i - 1]) >= 0)) nums.Add(u + 1);
            }
            return nums;
        }

        /// What the line names that the facts do not have; empty when it may pass. Wider adds numbers and listed nouns.
        public static List<string> Missing(string line, IEnumerable<string> facts, bool wider = false)
        {
            var factList = facts.ToList();
            var words = FactWords(factList);
            var missing = new List<string>();
            foreach (var run in Names(line))
            {
                var core = run.Where(w => !Titles.Contains(w.ToLowerInvariant()) && !Common.Contains(w.ToLowerInvariant())).ToList();
                if (core.Count > 0 && !core.Any(w => words.Contains(w.ToLowerInvariant()))) missing.Add(string.Join(" ", run));
            }
            if (!wider) return missing;
            var factNums = Numbers(string.Join(" ", factList));
            string low = (line ?? "").ToLowerInvariant();
            foreach (var n in Numbers(OneAsPronoun.Replace(low, " ")).Where(n => !factNums.Contains(n)).OrderBy(n => n)) missing.Add(n.ToString());
            foreach (Match m in Regex.Matches(low.Replace("'s", ""), "[a-z]+"))
            {
                string w = m.Value;
                if ((PlaceNouns.Contains(w) || RoleNouns.Contains(w)) && !words.Contains(w) && !words.Contains(w.TrimEnd('s'))) missing.Add(w);
            }
            return missing;
        }
    }
}
