using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// THE RULE TABLE FOR THE FIRST WEEK (Jafar's list of 30 September
    /// afternoon, item 4; the research note grounded-dialogue-selection, step 3,
    /// after Valve's response system). What the player says is sorted into a
    /// kind of question (a concept); for that concept and who is asked, the most
    /// specific rule decides between an answer, a partial answer, or "don't
    /// know, ask someone who does", and names the street's facts it rests on
    /// (StreetFacts, by id). Those facts, not the ones shared words would pick
    /// (ClaimCheck.Bearing), are put before the writer, and are what the
    /// character says plainly when the check refuses twice. A line of no
    /// concept, or of a concept that needs where they are or what nobody has
    /// written yet (Scene), keeps today's path.
    ///
    /// The concepts come from the sixty newcomer questions the talk was tuned
    /// on and the note's list (who are you, what is this place, where do I
    /// sleep, the door, the boss, money, the will, Mickey, trust, food, family,
    /// what now), never from the sets it is measured on.
    public static class TalkRules
    {
        public enum Kind { Answer, Partial, DontKnow, Scene }

        public sealed class Rule
        {
            public string Concept;
            /// Who is asked (a cast id), or null for anyone: a rule for the
            /// speaker is more specific than the general one, and wins.
            public string Speaker;
            public Kind Kind;
            public string[] Facts = new string[0];
            /// Somebody who would know, to point him to (a name as said).
            public string Ask;
        }

        /// What a rule gives the talk: its concept and kind, the facts in the
        /// words this speaker holds them in, and whom to point him to.
        public sealed class Choice
        {
            public string Concept;
            public Kind Kind;
            public List<string> Facts = new List<string>();
            public string Ask;
        }

        static Regex R(string pattern) => new Regex(pattern, RegexOptions.IgnoreCase | RegexOptions.Compiled);

        // In order: the first that matches is the concept.
        // In order: the first that matches is the concept. Narrow on purpose (the
        // blind review of 30 September: "Leave me alone" was read as the will,
        // "Did Mickey die in his sleep?" as where he sleeps, "Is the cafe any
        // good?" as the business, "Who's at the door?" as Mickey's room).
        const string End = @"\s*[?.!]*\s*$";
        static readonly (string concept, Regex pattern)[] Concepts =
        {
            ("funeral", R(@"\bfuneral\b")),
            ("mickey_death", R(@"\bhow did (mickey|he) die\b|\bwhat happened to mickey\b(?!')|\bwhat killed (him|mickey)\b|\bhow (did )?mickey (die|go)\b")),
            ("mickey_like", R(@"\bwhat was mickey like\b|\btell me about mickey\b(?!')|\bwhat (sort|kind) of (man|bloke|person) was (mickey|he)\b")),
            ("family", R(@"\b(mickey'?s|his) family\b|\bdid (mickey|he) have (any )?(family|relatives)\b")),
            ("inheritance", R(@"\b(did|has) (he|mickey) (leave|left) me\b|\bleft me (the|his|anything)\b|\binherit|\bthe will\b|\bin his will\b")),
            ("door", R(@"\b(back|locked|that|his|mickey'?s) door\b|\bback room\b")),
            ("sleep", R(@"\bwhere (do|will|can|am) i (sleep|sleeping|stay|staying|live|living|kip)\b|\bwhere('s| is) my (bed|room)\b")),
            ("who_runs", R(@"\bwho runs (the office|mickey'?s|this place|things)\b|\bruns things\b|\bwho('s| is) the boss\b")),
            ("money", R(@"\bany money in\b|\bmaking (any )?money\b|\btakings\b|\b(business|office|place) any good\b|\bbusiness doing\b")),
            ("drivers", R(@"\bdrivers\b|\bhow many (cabs|cars)\b")),
            ("office_where", R(@"\bwhere('s| is) (the office|mickey'?s)" + End)),
            ("work_for_me", R(@"\b(will|do|are) you (going to )?work(ing)? for me\b")),
            ("food", R(@"\b(something|anything|somewhere) to eat\b|\bget (some )?food\b|\bi'?m (starving|hungry)\b")),
            ("who_are_you", R(@"\bwho are you" + End + @"|\bwho're you" + End + @"|\bwhat('s| is) your name\b")),
            ("what_you_do", R(@"\bwhat do you do( here| round here| for a living)?" + End + @"|\bwhat('s| is) your job\b")),
            ("my_job", R(@"\bwhat am i (meant|supposed) to do\b|\bwhat should i do\b|\bwhat do i do\b")),
            ("what_place", R(@"\bwhat('s| is) this place\b|\bwhere am i" + End)),
            ("trust", R(@"\bwho can i trust\b|\bwho do i trust\b|\bcan i trust\b")),
            ("anything_know", R(@"\banything( else)? i should know\b|\bwhat( else)? should i know\b")),
            ("what_now", R(@"\bwhat happens now\b|\bwhat now\b")),
        };

        static readonly Rule[] Rules =
        {
            // Partial: "Were you at the funeral?" is not answered by where it was.
            new Rule { Concept = "funeral", Kind = Kind.Partial, Facts = new[] { "funeral", "june" } },
            new Rule { Concept = "mickey_death", Kind = Kind.Answer, Facts = new[] { "died_heart", "died_when" } },
            // What Mickey was like: only what Jafar approved (30 September), and
            // that is all they can tell him.
            new Rule { Concept = "mickey_like", Kind = Kind.Partial, Facts = new[] { "mickey_counsel", "mickey_kept_ron" } },
            new Rule { Concept = "family", Kind = Kind.Answer, Facts = new[] { "june" } },
            new Rule { Concept = "inheritance", Kind = Kind.Answer, Facts = new[] { "will", "flat" } },
            new Rule { Concept = "door", Kind = Kind.Answer, Facts = new[] { "door" } },
            new Rule { Concept = "sleep", Kind = Kind.Answer, Facts = new[] { "flat" } },
            // Partial: past the office, in a town with its outfits, they could not say.
            new Rule { Concept = "who_runs", Kind = Kind.Partial, Facts = new[] { "will", "sheila_books", "ron_rank" } },
            new Rule { Concept = "money", Kind = Kind.Partial, Facts = new[] { "trade" }, Ask = "Sheila" },
            new Rule { Concept = "money", Speaker = "lena", Kind = Kind.Answer, Facts = new[] { "trade", "sheila_books" } },
            new Rule { Concept = "drivers", Kind = Kind.Answer, Facts = new[] { "drivers", "hours" } },
            new Rule { Concept = "office_where", Kind = Kind.Answer, Facts = new[] { "office" } },
            new Rule { Concept = "work_for_me", Kind = Kind.Scene },
            new Rule { Concept = "work_for_me", Speaker = "lena", Kind = Kind.Partial, Facts = new[] { "sheila_books", "will" } },
            new Rule { Concept = "work_for_me", Speaker = "rocco", Kind = Kind.Partial, Facts = new[] { "ron_rank", "will" } },
            new Rule { Concept = "food", Kind = Kind.Answer, Facts = new[] { "cafe" } },
            new Rule { Concept = "who_are_you", Kind = Kind.Scene },
            new Rule { Concept = "who_are_you", Speaker = "lena", Kind = Kind.Answer, Facts = new[] { "sheila_books" } },
            new Rule { Concept = "who_are_you", Speaker = "rocco", Kind = Kind.Answer, Facts = new[] { "ron_rank" } },
            new Rule { Concept = "who_are_you", Speaker = "sam", Kind = Kind.Answer, Facts = new[] { "darren_rounds" } },
            new Rule { Concept = "what_you_do", Kind = Kind.Scene },
            new Rule { Concept = "what_you_do", Speaker = "lena", Kind = Kind.Answer, Facts = new[] { "sheila_books" } },
            new Rule { Concept = "what_you_do", Speaker = "rocco", Kind = Kind.Answer, Facts = new[] { "ron_rank" } },
            new Rule { Concept = "what_you_do", Speaker = "sam", Kind = Kind.Answer, Facts = new[] { "darren_rounds" } },
            new Rule { Concept = "my_job", Kind = Kind.Partial, Facts = new[] { "will" }, Ask = "Sheila" },
            new Rule { Concept = "my_job", Speaker = "lena", Kind = Kind.Partial, Facts = new[] { "will", "sheila_books" } },
            // Where they are, and whom they trust, are theirs to say from the scene and their card.
            new Rule { Concept = "what_place", Kind = Kind.Scene },
            new Rule { Concept = "trust", Kind = Kind.Scene },
            new Rule { Concept = "anything_know", Kind = Kind.Partial, Facts = new[] { "trade", "hours" } },
            new Rule { Concept = "what_now", Kind = Kind.Partial, Facts = new[] { "will" }, Ask = "Sheila" },
            new Rule { Concept = "what_now", Speaker = "lena", Kind = Kind.Partial, Facts = new[] { "will", "sheila_books" } },
        };

        // The first-week speakers by the names the street says.
        static string NameOf(string speaker) =>
            speaker == "lena" ? "Sheila" : speaker == "rocco" ? "Ron" : speaker == "sam" ? "Darren" : null;

        /// Kinds of question whose answer is the speaker themselves: said
        /// plainly without an opener ("All I know is this, boss. I keep the
        /// rank" read oddly).
        public static bool AboutThemselves(string concept) => concept == "who_are_you" || concept == "what_you_do";

        /// The kind of question a line is, or null for none of them.
        public static string ConceptOf(string line)
        {
            if (string.IsNullOrWhiteSpace(line)) return null;
            foreach (var (concept, pattern) in Concepts)
                if (pattern.IsMatch(line)) return concept;
            return null;
        }

        /// The most specific rule for what he said and who is asked (a rule
        /// for the speaker over the general one), or null when the line is of
        /// no concept. A speaker is never pointed to themselves.
        public static Choice Choose(string line, string speaker)
        {
            var concept = ConceptOf(line);
            if (concept == null) return null;
            Rule best = null;
            foreach (var r in Rules)
            {
                if (r.Concept != concept || (r.Speaker != null && r.Speaker != speaker)) continue;
                if (best == null || (r.Speaker != null && best.Speaker == null)) best = r;
            }
            if (best == null) return null;
            // Never pointed to themselves (the blind review: the rules kept it so
            // only by luck).
            string ask = best.Ask != null && NameOf(speaker) == best.Ask ? null : best.Ask;
            var choice = new Choice { Concept = concept, Kind = best.Kind, Ask = ask };
            foreach (var id in best.Facts)
            {
                var text = StreetFacts.Held(id, speaker);
                if (text != null) choice.Facts.Add(text);
            }
            return choice;
        }
    }
}
