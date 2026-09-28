using System.Collections.Generic;

namespace Ledger.Core
{
    /// WHAT THE PLAYER JUST ASSERTED, IF ANYTHING.
    ///
    /// WHY THIS EXISTS. `ConversationEngine.ProcessClaim` checks a claim
    /// against what somebody knows, raises suspicion on a contradiction and
    /// lowers it when the story checks out. `GossipMill.PlayerClaims` records
    /// what the player has told people so the street can carry it. Both are
    /// written, both are tested in `SimHarness`, and both have sat on the reach
    /// ledger with the same note: *"the player asserting something the street
    /// can then carry is the spine of `law as a tool`, and nothing in the game
    /// yet lets them make a claim."*
    ///
    /// Nothing let them make a claim because nothing turned a sentence into a
    /// `Fact`. That is this file, and it is the missing inch between a typed
    /// line and the entire information layer.
    ///
    /// LEXICAL, NOT MODEL. The router asks a model when a lexical pass fails,
    /// and this deliberately does not. A claim moves suspicion and enters the
    /// permanent record of what the player has said; a model that hallucinates
    /// one produces an alibi the player never gave, gets caught contradicting a
    /// witness, and raises suspicion over a sentence that was never typed. A
    /// missed claim costs nothing and can be typed again. The two errors are
    /// not remotely symmetric, so this only fires on shapes it is sure of.
    ///
    /// THE PLACES COME FROM THE CALLER. A vocabulary invented here would drift
    /// from the map the moment a district is added — the same fault as a metric
    /// whose scope is "every TextMesh in the scene". The game passes the names
    /// it actually has.
    public static class Claims
    {
        /// The key `Fact` has always used for where somebody was, quoted from
        /// the example in `Fact`'s own summary and from the harness that has
        /// exercised this path for months: `player.location_d2_evening`.
        public static string LocationKey(GameTime when) =>
            $"location_d{when.Day}_{when.Slot.ToString().ToLowerInvariant()}";

        /// The openers that mean "I am telling you where I was". First person
        /// and past tense, both required.
        ///
        /// "were you at" and "he was at" must not match, and that is not
        /// pedantry: a question is the opposite of a claim, and attributing
        /// somebody else's whereabouts to the player would file an alibi they
        /// never offered.
        static readonly string[] Openers =
        {
            "i was at ", "i was in ", "i was over at ", "i was round at ",
            "i was down at ", "i was up at ", "ive been at ", "i have been at ",
            "i spent the evening at ", "i spent the night at ",
        };

        // WRITTEN THE WAY THE INPUT ARRIVES, NOT THE WAY IT IS TYPED. `Extract`
        // strips apostrophes before matching, so an opener spelled "i've been
        // at" can never match anything — the normalisation happens on one side
        // of a comparison and the table has to live on that side too. Caught by
        // the test named for the tense, which is what tests in a compiling
        // layer are for.

        /// CHECK A CLAIM AGAINST WHAT SOMEBODY KNOWS, and move their suspicion.
        ///
        /// LIFTED OUT OF `ConversationEngine` BECAUSE IT WAS UNREACHABLE THERE.
        /// The sim runs with no LLM client, so a `ConversationHost` never builds
        /// its engine — and this method, which touches only knowledge,
        /// suspicion and memory and needs no model at all, was hanging off that
        /// object. `claimVia=[game.Hosts] claimWhy=[not tried]` was the two
        /// facts side by side: the host was found and its engine was null.
        ///
        /// So the one thing in the conversation layer that is pure bookkeeping
        /// could not run in the one place that exercises the game unattended.
        /// `ConversationEngine.ProcessClaim` now delegates here, so there is one
        /// implementation and the caller decides whether it needs a model.
        ///
        /// `weight` scales how far suspicion moves: 1.0 across a table,
        /// `PhoneBook.Damped(1.0)` down a wire.
        public static ClaimResult Process(KnowledgeBase knowledge, SuspicionTracker suspicion,
                                          MemoryStore memory, Fact claim, GameTime now,
                                          double weight = 1.0)
        {
            if (knowledge == null || claim == null) return ClaimResult.Unknown;
            var result = knowledge.CheckClaim(claim);
            weight = Feel.Clamp(weight, 0.0, 1.0);
            if (result == ClaimResult.Contradiction)
            {
                suspicion?.Raise(0.15 * weight,
                    weight < 1.0
                        ? $"caught contradiction on {claim.Subject}.{claim.Predicate}, on the telephone"
                        : $"caught contradiction on {claim.Subject}.{claim.Predicate}");
                memory?.Append(new MemoryEvent(now, "observation", 0.8,
                    $"The player claimed {claim} but I know otherwise. They lied to me."));
            }
            else if (result == ClaimResult.Consistent)
            {
                suspicion?.Lower(0.03 * weight, "story checked out");
            }
            return result;
        }

        /// The vocabulary, built from the map the game actually has.
        ///
        /// Two forms per place: the full name without its article — "hook
        /// street pub" — and the last word, "pub", because that is how people
        /// speak. The short form is only registered when it is UNIQUE: three
        /// places on this map end in "corner", and letting the north corner
        /// answer to "corner" would file an alibi naming a place the player did
        /// not say. An ambiguous alibi is worse than none, because it can be
        /// contradicted by a witness to a different place entirely.
        public static Dictionary<string, string> KnownPlaces()
        {
            var full = new Dictionary<string, string>();
            var shortCount = new Dictionary<string, int>();
            var shortId = new Dictionary<string, string>();
            foreach (var p in HookMap.Places)
            {
                if (p == null || string.IsNullOrEmpty(p.Name)) continue;
                string n = p.Name.ToLowerInvariant();
                if (n.StartsWith("the ", System.StringComparison.Ordinal)) n = n.Substring(4);
                full[n] = p.Id;
                int sp = n.LastIndexOf(' ');
                string last = sp < 0 ? n : n.Substring(sp + 1);
                shortCount[last] = shortCount.TryGetValue(last, out var c) ? c + 1 : 1;
                shortId[last] = p.Id;
            }
            foreach (var kv in shortCount)
                if (kv.Value == 1 && !full.ContainsKey(kv.Key)) full[kv.Key] = shortId[kv.Key];
            return full;
        }

        /// WHEN THE DEED WAS, and which day it is now, for reading whether a time
        /// named in talk is the deed's (the independent check's fourth pass: their
        /// "where were you around eleven, when the window went?" is about an
        /// eleven o'clock deed). Unknown, the default, reads every time as another.
        public readonly struct DeedWhen
        {
            public readonly int Day, Hour, Today;
            public readonly bool Known;
            public DeedWhen(int day, int hour, int today) { Day = day; Hour = hour; Today = today; Known = day >= 0 && hour >= 0; }
            /// The small hours belong to the night before.
            public int NightDay => Hour < 6 ? Day - 1 : Day;
            /// The weekday of the deed's night ("Tuesday" for 02:00 on Wednesday).
            public string Weekday => Known ? new GameTime(NightDay, 12, 0).WeekdayName : null;
            /// The weekday of the deed's own day ("Wednesday" for 02:00 on Wednesday).
            public string DayWeekday => Known ? new GameTime(Day, 12, 0).WeekdayName : null;
        }

        /// WHERE HE SAYS HE WAS, as areas (town list 6ac, after the independent
        /// check found true answers read as lies): from each plain sentence that
        /// opens as a first-person past claim ("I was at", "I've been at"), every
        /// area it names, so "the chapel, then Rita's" is both. Never a question,
        /// a denial, reported speech ("who says I was at", "she told you"), a
        /// supposition ("if I was at") or a sentence that names another time
        /// ("this morning", "yesterday"). Empty when none.
        public static HashSet<string> WhereHeSays(string said, IDictionary<string, HashSet<string>> spokenAreas) =>
            WhereHeSays(said, spokenAreas, default, false, out _);

        static readonly System.Text.RegularExpressions.Regex TimeWordRx = new System.Text.RegularExpressions.Regex(
            @"(?<= )(this morning|this afternoon|this evening|today|tonight|last night|yesterday|earlier|tomorrow|last week|lunchtime|lunch|breakfast|dinner time|dinnertime|after work|before work|before you came|just now|a minute ago)(?= )");
        static readonly string[] HourWords = { "twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven" };
        // A number word is a clock time only after a word that makes it one, or
        // before one ("no one saw you" names no time).
        static readonly System.Text.RegularExpressions.Regex ClockWordRx = new System.Text.RegularExpressions.Regex(
            @"(?<= )(?:(?:at|around|about|gone|after|before|till|until|by|nearly|since|from|half|past|quarter to|round|near) (twelve|one|two|three|four|five|six|seven|eight|nine|ten|eleven)(?! (?:of|another|point|thing|way|day|minute|second|bit|or two|more|last))|(twelve|one|two|three|four|five|six|seven|eight|nine|ten|eleven) (?:oclock|am|pm|thirty|fifteen|forty|in the morning|at night))(?= )");

        static bool TimeWordFits(string w, DeedWhen d)
        {
            if (!d.Known) return false;
            int h = d.Hour;
            switch (w)
            {
                case "today": case "earlier": case "just now": case "a minute ago": case "before you came": return d.Day == d.Today;
                case "this morning": return d.Day == d.Today && h < 12;
                case "this afternoon": return d.Day == d.Today && h >= 12 && h < 18;
                case "this evening": return d.Day == d.Today && h >= 17;
                case "tonight": return d.NightDay == d.Today && (h >= 17 || h < 6);
                case "last night": return d.NightDay == d.Today - 1 && (h >= 17 || h < 6);
                case "yesterday": return d.Day == d.Today - 1 || d.NightDay == d.Today - 1;
                case "lunch": case "lunchtime": return h >= 11 && h < 15;
                case "dinner time": case "dinnertime": return (h >= 11 && h < 15) || (h >= 17 && h < 21);
                case "breakfast": return h >= 6 && h < 10;
                case "after work": return h >= 17 || h < 6;
                case "before work": return h >= 5 && h < 9;
                default: return false;
            }
        }

        // Within an hour of the deed's: on the twenty-four-hour clock when the
        // number or the words say which half of the day ("11am", "eleven at
        // night"; the fifth pass: "at 11am" was taken for an 11 pm deed), else
        // on a twelve-hour clock ("around eleven" for 23:00).
        static bool HourFits(int clock, DeedWhen d, string half)
        {
            if (!d.Known || half == "both") return false;
            if (clock > 12 || half != null)
            {
                int h24 = clock > 12 ? clock % 24 : half == "am" ? clock % 12 : clock % 12 + 12;
                int diff24 = ((h24 - d.Hour) % 24 + 24) % 24;
                return diff24 <= 1 || diff24 == 23;
            }
            int diff = ((clock - d.Hour) % 12 + 12) % 12;
            return diff == 0 || diff == 1 || diff == 11;
        }

        // Which half of the day the words give a clock time: "am", "pm", "both"
        // (they disagree) or null.
        static string HalfOfDay(string s)
        {
            bool am = System.Text.RegularExpressions.Regex.IsMatch(s, @" (am|in the morning|this morning) ");
            bool pm = System.Text.RegularExpressions.Regex.IsMatch(s, @" (pm|in the afternoon|in the evening|at night|this afternoon|this evening|tonight|last night) ");
            return am && pm ? "both" : am ? "am" : pm ? "pm" : null;
        }

        static string Letters(string text) =>
            " " + System.Text.RegularExpressions.Regex.Replace(
                (text ?? "").ToLowerInvariant().Replace("a.m.", "am").Replace("p.m.", "pm").Replace("'", "").Replace("\u2019", ""),
                @"[^a-z]+", " ").Trim() + " ";

        // Words for a whole day, or for a part of one with no day to it.
        static readonly HashSet<string> LooseWords = new HashSet<string>
            { "today", "yesterday", "earlier", "lunch", "lunchtime", "breakfast", "dinner time", "dinnertime", "after work", "before work", "just now", "a minute ago", "before you came" };

        /// WHETHER A QUESTION'S TIME IS TOO LOOSE for a plain answer to be judged
        /// against one hour (the fifth pass: "where were you yesterday?" and his
        /// true "I was at the cafe", there in the day): it names a whole day, a
        /// part of one with no day ("after work"), or a weekday with no part of
        /// it, and nothing narrower. No time at all is not loose: they are asking
        /// about the deed.
        public static bool LooseTime(string text, DeedWhen deed)
        {
            if (string.IsNullOrEmpty(text)) return false;
            string s = Letters(text);
            bool loose = false, narrow = false;
            foreach (System.Text.RegularExpressions.Match m in TimeWordRx.Matches(s))
                if (LooseWords.Contains(m.Value)) loose = true; else narrow = true;
            if (System.Text.RegularExpressions.Regex.IsMatch(text, @"\d") || ClockWordRx.IsMatch(s)
                || System.Text.RegularExpressions.Regex.IsMatch(s, @" (midnight|noon|midday) "))
                narrow = true;
            foreach (var wd in new[] { "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday" })
                if (s.Contains(" " + wd + " "))
                {
                    if (System.Text.RegularExpressions.Regex.IsMatch(s, " " + wd + " (night|evening|morning|afternoon) ")) narrow = true;
                    else loose = true;
                }
            return loose && !narrow;
        }

        /// WORDS FOR ANOTHER TIME than the deed's, as the answer and their
        /// question are both read (the independent check's third and fourth
        /// passes): a part of a day, a clock time or a weekday that is not the
        /// deed's; with the deed unknown, any of them.
        public static bool NamesAnotherTime(string text, DeedWhen deed)
        {
            if (string.IsNullOrEmpty(text)) return false;
            string s = Letters(text);
            string half = HalfOfDay(s);
            foreach (System.Text.RegularExpressions.Match m in System.Text.RegularExpressions.Regex.Matches(text, @"\d+(?:[:.]\d\d)?"))
            {
                string n = m.Value.Split(':', '.')[0];
                if (n.Length > 2 || !int.TryParse(n, out int v) || v > 24 || !HourFits(v, deed, half)) return true;
            }
            foreach (System.Text.RegularExpressions.Match m in TimeWordRx.Matches(s))
                if (!TimeWordFits(m.Value, deed)) return true;
            foreach (System.Text.RegularExpressions.Match m in ClockWordRx.Matches(s))
            {
                string w = m.Groups[1].Success ? m.Groups[1].Value : m.Groups[2].Value;
                if (!HourFits(System.Array.IndexOf(HourWords, w), deed, half)) return true;
            }
            if (System.Text.RegularExpressions.Regex.IsMatch(s, @" midnight ") && !HourFits(24, deed, null)) return true;
            if (System.Text.RegularExpressions.Regex.IsMatch(s, @" (noon|midday) ") && !HourFits(12, deed, "pm")) return true;
            // A weekday, with its part of the day when it has one, read against the
            // deed's hour as "this morning" is (the sixth pass: "Tuesday afternoon"
            // was taken for a deed at 23:00 on Tuesday).
            foreach (var wd in new[] { "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday" })
            {
                if (!s.Contains(" " + wd + " ")) continue;
                bool night = string.Equals(wd, deed.Weekday, System.StringComparison.OrdinalIgnoreCase);
                bool own = string.Equals(wd, deed.DayWeekday, System.StringComparison.OrdinalIgnoreCase);
                if (!deed.Known) return true;
                int h = deed.Hour;
                var parts = System.Text.RegularExpressions.Regex.Matches(s, "(?<= )" + wd + " (morning|afternoon|evening|night)(?= )");
                if (parts.Count == 0 && !(night || own)) return true;
                // Every one named, not only the first ("Tuesday night, or was it Tuesday morning?").
                foreach (System.Text.RegularExpressions.Match part in parts)
                {
                    string w = part.Groups[1].Value;
                    bool fits = w == "morning" ? own && h < 12
                        : w == "afternoon" ? own && h >= 12 && h < 18
                        : w == "evening" ? own && h >= 17
                        : night && (h >= 17 || h < 6);
                    if (!fits) return true;
                }
            }
            return false;
        }

        /// Openers for a bare answer to "where were you?": "At the chapel."
        static readonly string[] BareOpeners = { "at ", "in ", "down at ", "up at ", "over at ", "round at ", "the " };

        // Words around an answer, not another sentence of it: "Me? I was at the
        // chapel." is one answer (the fourth pass).
        static readonly System.Text.RegularExpressions.Regex FillerRx = new System.Text.RegularExpressions.Regex(
            @"^ ((me|no|nah|yes|yeah|aye|honest|honestly|mate|pal|love|look|listen|well|eh|what|why|sorry|right|alright|ok|okay|course|of course|straight up|i swear) )+$");

        // PLAIN: one place and nothing after it but how long he was there, or
        // the deed's night (a night that is not the deed's never gets this far).
        static readonly System.Text.RegularExpressions.Regex PlainRx = new System.Text.RegularExpressions.Regex(
            @"^\s*(the\s+)?#(\s+(all night|all evening|the whole night|the whole time|the whole evening|that night|at the time|all the time|last night|tonight|this evening|on (monday|tuesday|wednesday|thursday|friday|saturday|sunday) (night|evening)))*(\s+(honest|mate|pal|love|i swear))?\s*$");

        /// As above, and `definite` is true only for a one-sentence answer naming
        /// one place and nothing else ("I was at the chapel all night"): only a
        /// definite answer can check out or be caught as a lie. With
        /// `answeringWhere`, a sentence that is only a place ("At the chapel, all
        /// night.") is his answer too, because they have just asked.
        public static HashSet<string> WhereHeSays(string said, IDictionary<string, HashSet<string>> spokenAreas, DeedWhen deed, bool answeringWhere, out bool definite)
        {
            definite = false;
            var areas = new HashSet<string>();
            if (string.IsNullOrWhiteSpace(said) || spokenAreas == null) return areas;
            string text = said.Replace('\u2019', '\'').Replace('\u2018', '\'');
            var names = new List<string>(spokenAreas.Keys);
            names.RemoveAll(n => n.Length == 0);
            names.Sort((x, y) => y.Length.CompareTo(x.Length));
            int claims = 0, sentences = 0; bool plain = false;
            foreach (var raw in System.Text.RegularExpressions.Regex.Split(text, @"(?<=[.!?])\s+"))
            {
                var sentence = raw.Trim();
                if (sentence.Length == 0) continue;
                // Every non-letter a space: a dash, a colon or a quotation mark must
                // not hide a place (the second pass).
                string s = " " + System.Text.RegularExpressions.Regex.Replace(sentence.ToLowerInvariant().Replace("'", ""), @"[^a-z]+", " ").Trim() + " ";
                if (FillerRx.IsMatch(s)) continue;
                sentences++;
                if (sentence.EndsWith("?")) continue;
                if (System.Text.RegularExpressions.Regex.IsMatch(s, @" (never|wasnt|was not|nowhere near|if|says|said|told|tell|reckon|think|thinks|suppose|maybe|might) "))
                    continue;
                // A part of a day, a clock time or a day that is not the deed's: another time.
                if (NamesAnotherTime(sentence, deed)) continue;
                int at = -1, len = 0; bool bare = false;
                foreach (var opener in Openers)
                {
                    int i = s.IndexOf(" " + opener, System.StringComparison.Ordinal);
                    if (i >= 0 && (at < 0 || i < at)) { at = i; len = opener.Length; }
                }
                // A bare place, answering their question, from the sentence's start.
                if (at < 0 && answeringWhere)
                    foreach (var opener in BareOpeners)
                        if (s.StartsWith(" " + opener, System.StringComparison.Ordinal)) { at = 0; len = opener == "the " ? 0 : opener.Length; bare = true; break; }
                if (at < 0) continue;
                // Every place the sentence names, before the opener as well as after
                // it: "after the chapel I was at Rita's" names two (the fourth pass).
                string head = s.Substring(0, at) + " ";
                string tail = " " + s.Substring(at + 1 + len) + " ";
                var here = new HashSet<string>();
                int before = 0, after = 0;
                foreach (var name in names)
                {
                    var rx = new System.Text.RegularExpressions.Regex(@"(?<=\s)" + System.Text.RegularExpressions.Regex.Escape(name) + @"(?=\s)");
                    if (rx.IsMatch(head)) { here.UnionWith(spokenAreas[name]); before++; head = rx.Replace(head, "#"); }
                    if (rx.IsMatch(tail)) { here.UnionWith(spokenAreas[name]); after++; tail = rx.Replace(tail, "#"); }
                }
                bool plainHere = before == 0 && after == 1 && PlainRx.IsMatch(tail);
                // A bare answer is only a place: "The rank was empty when I left" is not one.
                if (bare && !plainHere) continue;
                claims++;
                areas.UnionWith(here);
                if (plainHere) plain = true;
            }
            // One sentence, one claim, one place: "I was at the chapel. Then Rita's."
            // is not definite (the third pass).
            definite = sentences == 1 && claims == 1 && plain;
            return areas;
        }

        /// Turn a typed line into a claim about where the player was, or null.
        ///
        /// `places` maps a spoken name to the id the world uses — "the anchor"
        /// to "anchor" — so the caller owns the vocabulary and this owns the
        /// grammar.
        public static Fact Extract(string said, GameTime now, IDictionary<string, string> places)
        {
            if (string.IsNullOrEmpty(said) || places == null) return null;
            string s = " " + said.ToLowerInvariant().Replace(",", " ").Replace(".", " ")
                                 .Replace("'", "").Replace("  ", " ");

            // A DENIAL IS NOT A CLAIM THIS MODEL CAN HOLD, and the reason is
            // worth writing down because the obvious encoding is actively
            // harmful. "I was never at the warehouse" would have to become a
            // value like `not_warehouse`, and `CheckClaim` compares values for
            // equality — so a witness who knows the player was at the CINEMA
            // would read `cinema != not_warehouse` as a contradiction and the
            // player would be caught lying about something they were telling
            // the truth about. Skipped, deliberately, until `Fact` can carry a
            // negation. Nothing is lost: the player simply has to say where
            // they were, which is what an alibi is.
            if (s.Contains(" never ") || s.Contains(" wasnt ") || s.Contains(" was not ")
                || s.Contains(" nowhere near "))
                return null;

            foreach (var opener in Openers)
            {
                // THE LEADING SPACE IS PART OF THE SEARCH AND NOT PART OF THE
                // OPENER. `s` is prefixed with a space so that "i was at" only
                // matches at a word boundary — otherwise "hawaii was at" would
                // — and the offset has to account for it. Getting this wrong by
                // one produced a tail of "t the anchor" and no match at all,
                // which the first test caught in a second because it is a Core
                // test rather than a 28-minute round trip.
                int i = s.IndexOf(" " + opener, System.StringComparison.Ordinal);
                if (i < 0) continue;
                string tail = s.Substring(i + 1 + opener.Length);
                foreach (var kv in places)
                {
                    if (string.IsNullOrEmpty(kv.Key)) continue;
                    string name = kv.Key.ToLowerInvariant();
                    // Anchored at the START of what follows the opener, so
                    // "I was at the pub after I left the docks" claims the pub
                    // and not the docks. The first place named after "I was at"
                    // is the one being claimed; everything after it is a story.
                    if (tail.StartsWith(name, System.StringComparison.Ordinal)
                        || tail.StartsWith("the " + name, System.StringComparison.Ordinal))
                        return new Fact("player", LocationKey(now), kv.Value);
                }
            }
            return null;
        }
    }
}
