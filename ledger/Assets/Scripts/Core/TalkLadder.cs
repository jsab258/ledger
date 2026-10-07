using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// THE LADDER BEFORE "THAT'S ALL I KNOW" (the talk task of 7 October 2026).
    /// On the fresh-question bench a third of the answers were "that's all I
    /// know" (23 to 25 of 60, 30 September) while the character held something
    /// that bore on the question: the writer reached for a true fact, added
    /// texture nobody wrote, and the check rightly refused it twice. Giving up
    /// there threw the true fact away with the texture.
    ///
    /// So when both drafts are refused, the character climbs before giving up,
    /// one rung a turn, never the same step twice to the same listener:
    ///   1. FACT: the next relevant fact they hold and have not told him, in the
    ///      plain words the street's facts carry (StreetFacts.SaidFor), after an
    ///      opener of their own. Relevant means the rule table chose it, or the
    ///      refused drafts cited it for what they got right (ClaimCheck.CitedItems):
    ///      the writer judges what bears on his line, code says it. Never a fact
    ///      chosen by shared words (measured on 30 September: 84 of 123 such lines
    ///      were beside the point), never a card's own fact or secret.
    ///   2. ASK: whom to ask: the rule table's (Sheila for the takings), or the
    ///      person a relevant fact is about, who holds it as their own. Never
    ///      themselves.
    ///   3. TOLD: who told them, for a story they only heard (the memory of the
    ///      telling names the teller: "I heard from Ada that ...").
    ///   4. REFUSE: a refusal in their own voice with a reason (loyalty, caution,
    ///      wanting paying), worded so it claims no knowledge they lack, and only
    ///      when he presses on what they have already given; with nothing relevant
    ///      ever given, their honest "that's all I know".
    /// Every line is built by code from facts and written lines, so nothing on
    /// the ladder is the model's and nothing needs checking; the deterministic
    /// side decides what is said, the model only judged what was relevant.
    public static class TalkLadder
    {
        /// One thing they know that bears on his question.
        public sealed class Lead
        {
            /// The item as they hold it (a fact's text, or a memory's).
            public string Key;
            /// Its plain words, or null when it is never said plainly.
            public string Said;
            /// Somebody else who holds it as their own, by name, or null.
            public string AskWho;
            /// Who told them, by name, for a story they heard, or null.
            public string ToldBy;
            /// A fact about the speaker themselves.
            public bool Own;
            /// It bears on his words: the rule table chose it, or it shares a
            /// telling word with his line (ClaimCheck.SharesTellingWord). Only such
            /// a lead is said, pointed to or named; the rest count only towards
            /// whether he is pressing on what they already gave him (the bait of 7
            /// October: asked for a poem, a draft that wandered to the locked door
            /// made the door the answer).
            public bool Bears = true;
        }

        // He asked who somebody is ("Who's Sheila?", "who was that?").
        static readonly Regex AsksWho = new Regex(@"\bwho('s|s| is| was| are| were)\b", RegexOptions.IgnoreCase);

        /// THE LEADS FOR ONE LINE: what bears on it, the rule table's facts first
        /// (its answer), then what the refused drafts cited, most cited first. A
        /// street fact goes with its plain words and whom it is about; a story they
        /// heard with who told them; nothing else is a lead. Somebody else's job
        /// is a pointer ("You'd want Sheila for that") unless he asked who
        /// somebody is or the rule table chose it; their own, said to another
        /// question, loses the name it opens on. `known` is everything they know,
        /// so a word common to half of it does not make a fact bear on his line.
        public static List<Lead> Leads(string line, CharacterCard card, IEnumerable<string> ruleFacts, bool aboutThemselves, IEnumerable<string> cited,
                                       IReadOnlyCollection<string> known = null)
        {
            var leads = new List<Lead>();
            var seen = new HashSet<string>();
            bool asksWho = AsksWho.IsMatch(line ?? "");
            void Add(string text, bool ruled)
            {
                if (string.IsNullOrEmpty(text) || !seen.Add(text)) return;
                var said = StreetFacts.SaidFor(text);
                if (said != null)
                {
                    var about = StreetFacts.AboutOf(text);
                    bool other = about != null && about != card.Id;
                    if (!other && StreetFacts.IsIntroduction(text) && !aboutThemselves && !asksWho)
                        said = WithoutOwnName(said, card.Name, StreetFacts.NameOf(card.Id));
                    leads.Add(new Lead
                    {
                        Key = text, Bears = ruled || ClaimCheck.SharesTellingWord(line, text, known),
                        Said = other && !ruled && StreetFacts.IsIntroduction(text) && !asksWho ? null : said,
                        Own = StreetFacts.IsOwn(text, card.Id), AskWho = other ? StreetFacts.NameOf(about) : null,
                    });
                    return;
                }
                var teller = HeardFrom(text);
                if (teller != null) leads.Add(new Lead { Key = text, ToldBy = teller, Bears = ClaimCheck.SharesTellingWord(line, text, known) });
            }
            if (ruleFacts != null) foreach (var f in ruleFacts) Add(f, true);
            if (cited != null) foreach (var text in cited) Add(text, false);
            return leads;
        }

        /// Leads as a run's record keeps them: "fact|", "ask|who|" or "told|who|"
        /// and the item, "unrelated " before one that shares nothing with his line.
        public static List<string> Describe(IEnumerable<Lead> leads)
        {
            var kept = new List<string>();
            foreach (var l in leads)
                kept.Add((l.Bears ? "" : "unrelated ") + (l.Said != null ? "fact" : l.AskWho != null ? "ask" : "told") + "|" + (l.AskWho ?? l.ToldBy ?? "") + "|" + l.Key);
            return kept;
        }

        /// What one turn on the ladder says: the rung ("fact", "ask", "told",
        /// "refuse"), the line, and what it has now told the listener (Marks);
        /// no rung and no line when they have nothing that bears on it.
        public sealed class Step
        {
            public string Rung;
            public string Line;
            public List<string> Marks = new List<string>();
        }

        /// The marks a listener's record keeps, one per thing told.
        public static string FactMark(string key) => "fact:" + key;
        static string AskMark(string who, string topic) => "ask:" + who + "|" + topic;
        static string ToldMark(string who, string topic) => "told:" + who + "|" + topic;

        /// THE SHARED WORDS, for anybody whose card has none of their own.
        /// The refusal is caution: it gives a reason and claims nothing.
        static readonly Dictionary<string, string[]> Shared = new Dictionary<string, string[]>
        {
            { "ask", new[] { "You'd want {who} for that.", "Ask {who}. Not me." } },
            { "told", new[] { "{who} told me. That's where I had it.", "I only had it from {who}." } },
            { "refuse", new[] { "I keep out of things like that, and I'd keep out of it if I were you.", "Not something I'd talk about. Leave it." } },
        };

        /// One of a card's own lines of a kind ("ask", "told", "refuse"), the
        /// `n`th time they need one, with the person put in; the shared words
        /// when the card has none. Where they start depends on who they are.
        public static string LineFor(CharacterCard card, string kind, int n, string who)
        {
            IReadOnlyList<string> lines = card?.Own(kind);
            if (lines == null || lines.Count == 0) lines = Shared.TryGetValue(kind, out var s) ? s : new string[0];
            if (lines.Count == 0) return "";
            uint h = 2166136261;
            foreach (char c in card?.Id ?? "") { h ^= c; h *= 16777619; }
            var line = lines[(int)((h + (uint)Math.Max(0, n)) % (uint)lines.Count)];
            return who == null ? line : line.Replace("{who}", who);
        }

        /// Their own plain words without the name they open on ("Sheila Dunn. I
        /// keep the books ..." becomes "I keep the books ..."): a sentence that
        /// is only their name, full or short, taken off the front.
        public static string WithoutOwnName(string said, string fullName, string shortName)
        {
            if (string.IsNullOrEmpty(said)) return said;
            foreach (var name in new[] { fullName, shortName })
                if (!string.IsNullOrWhiteSpace(name) && said.StartsWith(name.Trim() + ". ", StringComparison.Ordinal))
                    return said.Substring(name.Trim().Length + 2).TrimStart();
            return said;
        }

        static readonly Regex Stamp = new Regex(@"^\s*\[[^\]]*\]\s*");
        static readonly Regex HeardFromRx = new Regex(@"^(?:I )?heard from (?<who>[A-Z][\w'’ .-]*?) that\b", RegexOptions.IgnoreCase);
        static readonly Regex ToldWhenAskedRx = new Regex(@"^(?<who>[A-Z][\w'’ .-]*?) told me, when I asked:");

        /// WHO TOLD THEM, read from the memory of the telling as the gossip
        /// writes it ("I heard from Sheila that ...", "Darren told me, when I
        /// asked: ..."), a time stamp in front allowed; null for anything else.
        public static string HeardFrom(string memoryText)
        {
            if (string.IsNullOrWhiteSpace(memoryText)) return null;
            var t = Stamp.Replace(memoryText, "");
            var m = HeardFromRx.Match(t);
            if (!m.Success) m = ToldWhenAskedRx.Match(t);
            if (!m.Success) return null;
            var who = m.Groups["who"].Value.Trim();
            // "the shopkeeper" is nobody he can go and find by name.
            return who.Length == 0 || char.IsLower(who[0]) ? null : who;
        }

        /// ONE TURN ON THE LADDER. `told` says whether a mark is already in this
        /// listener's record. `ruleAsk` and `ruleTopic` are the rule table's whom
        /// to ask and its kind of question; `partial` that its facts answer only
        /// part of it (said with whom to ask for the rest, as measured on 30
        /// September); `aboutThemselves` that he asked about them, so their own
        /// facts come first and with no opener.
        public static Step Climb(IReadOnlyList<Lead> leads, Func<string, bool> told, CharacterCard card, string speakerName,
                                 string ruleAsk, string ruleTopic, bool partial, bool aboutThemselves, int n)
        {
            leads = leads ?? new List<Lead>();
            told = told ?? (_ => false);
            var step = new Step();

            // 1. THE NEXT RELEVANT FACT: somebody else's first, their own only
            // when it is all there is, unless he asked about them.
            Lead fact = null;
            foreach (var l in leads)
                if (l.Bears && l.Said != null && !told(FactMark(l.Key)) && (aboutThemselves || !l.Own)) { fact = l; break; }
            if (fact == null)
                foreach (var l in leads)
                    if (l.Bears && l.Said != null && !told(FactMark(l.Key))) { fact = l; break; }
            if (fact != null)
            {
                var openers = card?.Own("opener");
                string opener = aboutThemselves || openers == null || openers.Count == 0 ? "" : LineFrom(openers, card, n) + " ";
                string rest = "";
                if (partial)
                {
                    bool asked = ruleAsk != null && ruleAsk != speakerName && !told(AskMark(ruleAsk, ruleTopic));
                    rest = asked ? " You'd want " + ruleAsk + " for the rest." : " That's as much as I can tell you.";
                    if (asked) step.Marks.Add(AskMark(ruleAsk, ruleTopic));
                }
                step.Rung = "fact";
                step.Line = opener + fact.Said + rest;
                step.Marks.Add(FactMark(fact.Key));
                return step;
            }

            // 2. WHOM TO ASK: the rule table's, then whoever a relevant fact is about.
            if (ruleAsk != null && ruleAsk != speakerName && !told(AskMark(ruleAsk, ruleTopic)))
                return Said(step, "ask", LineFor(card, "ask", n, ruleAsk), AskMark(ruleAsk, ruleTopic));
            foreach (var l in leads)
                if (l.Bears && l.AskWho != null && l.AskWho != speakerName && !told(AskMark(l.AskWho, l.Key)))
                    return Said(step, "ask", LineFor(card, "ask", n, l.AskWho), AskMark(l.AskWho, l.Key));

            // 3. WHO TOLD THEM a story they only heard.
            foreach (var l in leads)
                if (l.Bears && l.ToldBy != null && l.ToldBy != speakerName && !told(ToldMark(l.ToldBy, l.Key)))
                    return Said(step, "told", LineFor(card, "told", n, l.ToldBy), ToldMark(l.ToldBy, l.Key));

            // 4. A REFUSAL WITH A REASON, in their own words, only at the top of a
            // climb: he is pressing on what they have already told him or sent him
            // elsewhere for. With nothing relevant ever given, they hold nothing
            // that bears on it, and the honest line is their "don't know" (null
            // here: the caller's). Measured on 7 October: a reason given to a
            // first, innocent question ("Where's the nearest phone box?" answered
            // "People remember who was asking") claimed a secret nobody keeps.
            bool pressed = ruleAsk != null && told(AskMark(ruleAsk, ruleTopic));
            foreach (var l in leads)
                if (told(FactMark(l.Key)) || (l.AskWho != null && told(AskMark(l.AskWho, l.Key))) || (l.ToldBy != null && told(ToldMark(l.ToldBy, l.Key))))
                    pressed = true;
            if (!pressed) return step;
            step.Rung = "refuse";
            step.Line = LineFor(card, "refuse", n, null);
            return step;
        }

        static Step Said(Step step, string rung, string line, string mark)
        {
            step.Rung = rung;
            step.Line = line;
            step.Marks.Add(mark);
            return step;
        }

        static string LineFrom(IReadOnlyList<string> lines, CharacterCard card, int n)
        {
            uint h = 2166136261;
            foreach (char c in card?.Id ?? "") { h ^= c; h *= 16777619; }
            return lines[(int)((h + (uint)Math.Max(0, n)) % (uint)lines.Count)];
        }
    }
}
