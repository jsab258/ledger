using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// Who the player is, and what this street calls them.
    ///
    /// Open since 24 July and delegated to me on the 27th. The name is **Tom
    /// Novak** — Mickey's sister's boy, back in town with one suitcase and a
    /// letter. NOWAK AND TOMMY since 24 September (Jafar's names ruling, canon's
    /// NAMES block): Novak and Toma survive only in saves made before it.
    ///
    /// WHY THIS ONE. It had to sit beside Sedlak, Brela, Farid, Hal and
    /// Donna without sounding like it came from a different game, and it had to
    /// survive being said out loud a thousand times. Novak is two syllables, hard
    /// to soften, and it is a WORD (willow, in the language the docks half-speak)
    /// — which is the kind of name a city shortens without affection.
    ///
    /// THE PART THAT IS ACTUALLY A DESIGN DECISION, and the reason this is a
    /// class rather than a constant: for two months the game has said "the new
    /// owner" everywhere, and I came to this expecting to find and replace it.
    /// That would have been wrong. **"The new owner" is not a placeholder. It is
    /// what people call you before they know you**, and this is a game about
    /// being known. So the name is something the street LEARNS, and what
    /// somebody calls you is a readout of where you stand with them:
    ///
    ///   the new owner  — they know the bar changed hands, not who you are
    ///   Nowak           — you are a fact on this street now
    ///   Tom          — they have decided about you, and it was fine
    ///   Tommy          — two or three people, ever
    ///
    /// That gradient costs nothing, uses relationship state that already exists,
    /// and turns "somebody used your first name" into a thing the player can
    /// notice happening. A find-and-replace would have thrown that away.
    public class PlayerIdentity
    {
        public string First = "Tom";
        public string Diminutive = "Tommy";
        public string Surname = "Nowak";
        /// What you are to somebody who has not placed you yet. Deliberately the
        /// same string the whole game already used.
        public string Unplaced = "the new owner";

        /// The uncle. Named in the founding premise; his book of debts is the
        /// inheritance, so his name is load-bearing and lives here too.
        public string BenefactorFirst = "Mickey";
        public string BenefactorRelation = "your mother's brother";

        public string Full => $"{First} {Surname}";

        /// Deliberately NOT gendered anywhere in the writing. The name works
        /// either way, the street mostly uses the surname, and that keeps a
        /// later "who are you" option free rather than costing a rewrite.
        public const string GenderNote = "unset by design; the street uses the surname";

        /// What this person calls you, from what they know and how they feel.
        ///
        /// `knowsName` is the gate — closeness cannot promote a stranger, because
        /// somebody can like the look of you and still not know what to call you.
        public string AddressBy(bool knowsName, double closeness)
        {
            if (!knowsName) return Unplaced;
            if (closeness >= 0.75) return Diminutive;
            if (closeness >= 0.45) return First;
            return Surname;
        }

        /// How the player is referred to in a rumor — third person, by whoever is
        /// passing it on. Talk travels further than acquaintance does, so a
        /// rumor about you can carry your surname into mouths that have never
        /// met you. That is exactly how a name gets around a district.
        public string InTalk(bool streetKnowsName) =>
            streetKnowsName ? Surname : Unplaced;

        /// The same answer, worked out from the mill itself.
        ///
        /// THE SECOND SITE. `GossipDirector` had this rule and Core did not, so
        /// every rumour written from Core — the racket rounds, which are the
        /// bulk of what the ledger screen shows in open mode — hardcoded "the
        /// new owner" and the district could never learn to say Novak on the
        /// one page where it matters most.
        ///
        /// It is here rather than copied into `Empire` because two places
        /// deciding separately whether the street has learned your name is how
        /// a panel ends up saying "Novak" in one line and "the new owner" in
        /// the next — the same fault, one layer up, that put a raw id into a
        /// witness account an hour ago.
        ///
        /// ANY, not all, which is the mechanic and not laziness: one person
        /// knowing your name is how the rest of them come to say it.
        public static bool StreetKnowsName(GossipMill mill)
        {
            if (mill == null) return false;
            foreach (var g in mill.Agents)
                if (KnowsName(g)) return true;
            return false;
        }

        public string InTalk(GossipMill mill) => InTalk(StreetKnowsName(mill));

        /// Does this person know what to call you? They do once they have
        /// remembered anything about you at all — which is the same moment the
        /// game starts treating them as somebody who has met you, so there is no
        /// second bookkeeping to keep in step.
        public static bool KnowsName(Gossiper g) =>
            g != null && g.Memory != null && g.Memory.Events.Count > 0;

        /// Convenience for the game layer: what this person calls you right now.
        /// HOW SOMEBODY KNOWS HIM, for their talk (town list 6s, the checklist
        /// sweep of 28 September): the cards said "I have never met Mickey's
        /// nephew" for the whole game.
        ///
        /// WHETHER THEY HAVE MET HIM is the game's to say (it knows who has been
        /// in a scene with him), or their own earlier talk with him; never read
        /// off familiarity, which the game sets for the whole cast from the
        /// first minute (the independent check: Ron was told on his first talk
        /// that he had met him and called him Tom). WHAT THEY CALL HIM to his
        /// face is the game's too, from the street's ladder, and only a name he
        /// goes by; "the new owner" when it sends none, since nobody has told
        /// them his name (the gate is knowing, not liking). Met only by their own
        /// talk, they have spoken with him before, no more.
        /// Somebody who has only heard of him would not know him by sight.
        /// The check does not read what a character says about the person they
        /// are talking to, so the line itself holds them to their memories.
        public string HowTheyKnowHim(bool met, bool heardOfHim, string calls, bool onlyTheirOwnTalk = false)
        {
            const string hold = " Say nothing about when, where or how often you have met him beyond what your memories say.";
            if (!met)
                return (heardOfHim
                    ? $"You have not met Mickey's nephew, {Unplaced}, but you have heard of him: his name is {Surname}. You would not know him by sight; to his face he is {Unplaced} until he says who he is."
                    : $"You have never met Mickey's nephew, {Unplaced}: you are speaking with him for the first time.") + " Do not talk as though you had met him before.";
            string name = calls == First || calls == Diminutive || calls == Surname || calls == Unplaced ? calls : Unplaced;
            return (onlyTheirOwnTalk
                ? $"You have spoken with Mickey's nephew, {Unplaced}, before: you call him {name}."
                : $"You have met Mickey's nephew, {Unplaced}, and you know him to speak to: you call him {name}.") + hold;
        }

        public string AddressBy(Gossiper g) =>
            g == null ? Unplaced : AddressBy(KnowsName(g), g.Loyalty);

        // WHAT THE TOWN CALLS HIM, BY KNOWING (town list 6ch; canon: "the new
        // owner, then Nowak, then Tom, then Tommy. The gate is knowing, not
        // liking"; carried until Jafar rules on his 30 September page). AddressBy
        // above runs on goodwill, so after one tea Ada said "Tommy"; this is the
        // rung by what they know of him: Nowak once they know his name; Tom once
        // they have talked with him on two different days, or at once if he asked
        // them to; Tommy for nobody in the first week. A step up never goes back
        // down (`before`). Sheila, who names him only on trust, is the talk's.
        public enum Rung { NewOwner = 0, Surname = 1, First = 2, Diminutive = 3 }

        /// Mickey's own people, who know his name from Mickey before he comes
        /// (the recommended answer on Jafar's 29 September page).
        public static readonly HashSet<string> MickeysOwn = new HashSet<string> { "lena", "rocco", "sam" };

        public static Rung RungByKnowing(bool knowsName, int daysTalked, bool askedFirstName, Rung before = Rung.NewOwner)
        {
            var r = Rung.NewOwner;
            if (knowsName || askedFirstName) r = Rung.Surname;
            if (askedFirstName || (knowsName && daysTalked >= 2)) r = Rung.First;
            return r > before ? r : before;
        }

        /// The rung a name the game sends stands on, or null for a name that is
        /// none of them.
        public Rung? RungOf(string calls)
        {
            var c = (calls ?? "").Trim();
            if (c.Length == 0) return null;
            if (string.Equals(c, Diminutive, StringComparison.OrdinalIgnoreCase)) return Rung.Diminutive;
            if (string.Equals(c, First, StringComparison.OrdinalIgnoreCase)) return Rung.First;
            if (string.Equals(c, Surname, StringComparison.OrdinalIgnoreCase) || string.Equals(c, "Mr " + Surname, StringComparison.OrdinalIgnoreCase)) return Rung.Surname;
            if (string.Equals(c, Unplaced, StringComparison.OrdinalIgnoreCase)) return Rung.NewOwner;
            return null;
        }

        public string CallsFor(Rung r) =>
            r == Rung.Diminutive ? Diminutive : r == Rung.First ? First : r == Rung.Surname ? Surname : Unplaced;

        // HIS NAME, GIVEN (read as owning up is: a whole sentence of the shape
        // and the words round it; never a question, somebody else's words or a
        // quotation): "I'm Tom.", "Tom Nowak, Mickey's nephew.", "The name's
        // Nowak."; and asked to use it: "Call me Tom.", "Tom's fine.".
        static string NameWords(string s) =>
            " " + System.Text.RegularExpressions.Regex.Replace((s ?? "").ToLowerInvariant().Replace('\u2019', '\'').Replace("'", ""), @"[^a-z]+", " ").Trim() + " ";
        const string NameLead = @"^ (hello |hi |hiya |morning |good morning |evening |good evening |afternoon |good afternoon |alright |right |well |so |yes |yeah |oh |look |sorry |and |how do you do |pleased to meet you |nice to meet you )*";
        const string NameTail = @"( (mickeys nephew|his nephew|the nephew|the new owner|by the way|then|love|mate|sheila|ron|darren|ada|thanks|thank you|pleased to meet you|nice to meet you|how do you do|here|mickeys lad|from the cab office|from the office|from mickeys|and ive taken over( from mickey)?|and im taking over( from mickey)?|and im taking on the office|and ive come to take over))* $";
        const string Name = @"(tom nowak|tom|nowak|mr nowak)";
        // With the words that say it is his name ("I'm", "the name's").
        static readonly System.Text.RegularExpressions.Regex GivesNameShape = new System.Text.RegularExpressions.Regex(NameLead +
            @"((im |i am |its |it is |the names |names |my names |my name is |name is |they call me |people call me |call me mr |call me |(im |i am )(mickeys nephew|mickeys lad|the new owner) )" + Name + @"|(toms|tom is|nowaks|nowak is|tom nowaks) the name)" + NameTail);
        // The name alone, as a whole sentence ("Tom." "Nowak, Tom Nowak.").
        static readonly System.Text.RegularExpressions.Regex BareName = new System.Text.RegularExpressions.Regex(@"^ (tom nowak|nowak tom nowak|tom|nowak)" + NameTail);
        // What may stand beside a bare name in the same sentence: saying who he
        // is ("Tom Nowak, Mickey's nephew.", "I'm the new owner, Tom Nowak.",
        // "Tom Nowak, from Mickey's.").
        static readonly System.Text.RegularExpressions.Regex SelfClause = new System.Text.RegularExpressions.Regex(
            @"^ ((and )?(im |i am )?(mickeys nephew|mickeys lad|the new owner|his nephew|the nephew)|from mickeys|from mickeys office|from the office|from the cab office|by the way|here|then|and you must be [a-z]+|you must be [a-z]+|and you are [a-z]+)( (then|love|mate))* $");
        // A pleasantry: after his name it is his introduction ("Tom Nowak,
        // pleased to meet you."); before a name it greets somebody called Tom
        // ("Nice to meet you, Tom.").
        static readonly System.Text.RegularExpressions.Regex Pleasantry = new System.Text.RegularExpressions.Regex(
            @"^ (pleased to meet you|nice to meet you|how do you do|good to meet you)( (then|love|mate))* $");
        // Quotations: somebody else's words, never his own giving (the third
        // review: British typists quote in single marks).
        static readonly System.Text.RegularExpressions.Regex Quoted = new System.Text.RegularExpressions.Regex(
            "\"[^\"]*\"|\u201c[^\u201d]*\u201d|\u2018[^\u2019]*\u2019|(?<![A-Za-z])'[^']*'(?![A-Za-z])");
        // A double or curly mark left open; a lone single mark is an elided
        // word ("'Morning.", "'Scuse me", the fourth review), not a quotation.
        static readonly System.Text.RegularExpressions.Regex OpenQuote = new System.Text.RegularExpressions.Regex(
            "[\"\u201c\u201d\u2018]");
        static readonly System.Text.RegularExpressions.Regex AsksFirstShape = new System.Text.RegularExpressions.Regex(NameLead +
            @"(call me tom|call me tommy|you can call me tom|just call me tom|please call me tom|its tom please|its just tom|it is just tom|tom will do|toms fine|tom is fine|just tom|tom please|no need for mr nowak|dont call me mr nowak)" + NameTail);
        // Somebody else's words, or a joke, in the same sentence.
        static readonly System.Text.RegularExpressions.Regex NotHisOwn = new System.Text.RegularExpressions.Regex(
            @" ((?!i )[a-z]+ (said|says|told me|reckons|calls)|joking|kidding|as if|yeah right) ");

        /// Whether his line gives his name, and whether it asks them to call him
        /// Tom: clause by clause, so a question after it ("I'm Tom, and you
        /// are?") or somebody else's words in another sentence ("I'm Tom
        /// Nowak. Mickey said you'd help.") do not spoil it (the independent
        /// check); the name alone only as a whole sentence ("Tom."), never a
        /// clause ("Thanks, Tom.").
        public static (bool gave, bool askedFirst) GivesName(string said)
        {
            if (string.IsNullOrWhiteSpace(said)) return (false, false);
            // Quoted words are set aside; a quotation left open spoils the line.
            said = Quoted.Replace(said, " ");
            if (OpenQuote.IsMatch(said)) return (false, false);
            bool gave = false, first = false;
            foreach (var raw in System.Text.RegularExpressions.Regex.Split(said, @"(?<=[.!?])\s+"))
            {
                var sentence = raw.Trim();
                if (sentence.Length == 0 || NotHisOwn.IsMatch(NameWords(sentence))) continue;
                bool question = sentence.Contains("?");
                var clauses = sentence.TrimEnd('.', '!', '?').Split(new[] { ',', ';', ':' }, StringSplitOptions.RemoveEmptyEntries);
                // The clause a question mark ends is the question; the rest may give it.
                int upTo = question ? clauses.Length - 1 : clauses.Length;
                bool bare = false, other = false, bareTom = false, please = false;
                for (int i = 0; i < upTo; i++)
                {
                    var w = NameWords(clauses[i]);
                    if (AsksFirstShape.IsMatch(w)) { gave = true; first = true; }
                    else if (GivesNameShape.IsMatch(w)) gave = true;
                    else if (BareName.IsMatch(w)) { bare = true; bareTom |= w == " tom "; }
                    else if (w == " please ") please = true;
                    // A pleasantry before the name greets somebody called Tom.
                    else if (Pleasantry.IsMatch(w)) { if (!bare) other = true; }
                    else if (!SelfClause.IsMatch(w)) other = true;
                }
                // The name alone, or beside only who he is ("Tom Nowak, Mickey's
                // nephew.", "Nowak, Tom Nowak."), never beside anything else
                // ("Thanks, Tom.", "Tom, Dick and Harry.", "Nice to meet you, Tom.").
                if (bare && !other) { gave = true; if (bareTom && please) first = true; }
            }
            return (gave, first);
        }

        /// HIS NAME AS THE STREET'S PLAIN FACT: told to somebody (the talk's
        /// `gaveName`), it is theirs first-hand, not a secret, passed on by the
        /// town's rounds; whoever holds it knows his name (the game then sends
        /// "knowsName"). Once a person. It never shows in anybody's manner.
        public const string NameTopic = "player.name";
        internal static bool IsNameStory(Rumor r) =>
            r != null && r.Content != null && r.Content.Subject == "player" && r.TopicKey == NameTopic;
        public bool NameTold(GossipMill mill, string who, GameTime at)
        {
            if (mill == null || string.IsNullOrEmpty(who) || !(mill.Get(who) is Gossiper g) || g.Rumors.Exists(r => IsNameStory(r) && r.Hops == 0)) return false;
            // TOLD, NOT SEEN, AND THEIRS FIRST-HAND (the port's independent check,
            // 30 September): through the mill's sighting, somebody who had heard
            // his name at full certainty was never made first-hand, kept the
            // teller as its source, was "told" again every time, and remembered
            // "I saw it myself". The story is made theirs here, in place when they
            // already hold it second-hand.
            var fact = new Fact("player", "name", Surname);
            string said = $"Mickey's nephew is called {Surname}";
            Rumor held = null;
            foreach (var r in g.Rumors) if (IsNameStory(r) && (held == null || r.Confidence > held.Confidence)) held = r;
            if (held == null)
                g.Rumors.Add(new Rumor { Content = fact, OriginId = who, Summary = said, Confidence = 1.0, Hops = 0, Sensitive = false });
            else
            {
                held.Content = fact;
                held.OriginId = who;
                held.Summary = said;
                held.Confidence = 1.0;
                held.Hops = 0;
                held.ToldById = null;
                held.Sensitive = false;
            }
            g.Knowledge.Learn(fact);
            g.Memory.Append(new MemoryEvent(at, "observation", 0.6, $"He told me himself: {said}"));
            return true;
        }
        public static bool HoldsHisName(Gossiper g) => g != null && g.Rumors.Exists(IsNameStory);

        public Dictionary<string, object> Capture() => new Dictionary<string, object>
        {
            { "first", First }, { "diminutive", Diminutive }, { "surname", Surname },
        };

        public void Restore(Dictionary<string, object> data)
        {
            if (data == null) return;
            var f = MiniJson.GetString(data, "first");
            var d = MiniJson.GetString(data, "diminutive");
            var s = MiniJson.GetString(data, "surname");
            if (!string.IsNullOrEmpty(f)) First = f;
            if (!string.IsNullOrEmpty(d)) Diminutive = d == "Toma" ? "Tommy" : d;   // names-gate: allow (an old save)
            if (!string.IsNullOrEmpty(s)) Surname = s == "Novak" ? "Nowak" : s;   // a save from before the names ruling; names-gate: allow
        }
    }
}
