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
