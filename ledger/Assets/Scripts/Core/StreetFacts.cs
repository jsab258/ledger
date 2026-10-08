using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// WHAT THE STREET KNOWS THAT NOBODY HAD WRITTEN (town list ck; decided 29
    /// September, DECISIONS). Asked a newcomer's twenty first questions,
    /// Sheila, Ron and Darren answered 38 of 60 with "that's all I know", for
    /// want of plain facts: the door Sheila does not open, the funeral, what
    /// Mickey left, where Tom sleeps, the drivers, the trade, where to eat.
    /// Written from canon and the story outline (Mickey dead three weeks; the
    /// letter; the funeral he missed; June back for it, wanting nothing; the
    /// dispatcher and the two drivers of the cast; the parade and the shops
    /// across from its north half; the office's hours), and given to every
    /// talking character as things they know. Never his name: the street
    /// learns that by the ladder (PlayerIdentity). How Mickey died and the
    /// warehouse fire as the street has it, as Jafar ruled on 30 September; never
    /// the fire's truth, and never why the docks went (the outline keeps that
    /// "underneath, never explained"). The person a fact is about knows it in
    /// their own words.
    ///
    /// SAID PLAINLY (Jafar's list of 30 September afternoon, item 2; the research
    /// note grounded-dialogue-selection, step 1): each fact also has the plain
    /// words a character says it in to the new owner, and the person it is about
    /// their own, for when the check refuses a reply twice
    /// (ConversationEngine.PlainFallback). Every specific in them is the fact's.
    public static class StreetFacts
    {
        /// (whom it is about, or "", the street's words, their own words, said
        /// plainly to him, and said plainly by the person it is about).
        public static readonly (string id, string about, string fact, string own, string said, string ownSaid)[] All =
        {
            ("died_when", "", "Mickey died three weeks before the new owner, his nephew, came to Quay Street.", null,
                 "Mickey died three weeks before you came.", null),
            // How Mickey died (Jafar, 30 September): his heart; nobody thinks otherwise.
            ("died_heart", "rocco", "Mickey died of his heart, at the office early one morning; Ron found him when he came on at the rank, and the doctor said it was his heart.",
                      "I found Mickey at the office early one morning, when I came on at the rank; the doctor said it was his heart.",
                      "Mickey died of his heart, the doctor said. Ron came on at the rank early one morning and found him at the office.",
                      "Mickey died of his heart, the doctor said. I came on at the rank early one morning and found him at the office."),
            // The warehouse fire as the street has it (Jafar, 30 September); the truth is never the street's.
            ("fire", "", "Last November, on a Saturday night, the importer's warehouse at the far end of the old warehouse row burned down; the evening paper called it arson, since it started in two places, but nobody was charged, and the street says the owner had it done for the insurance.", null,
                 // Said plainly without the street's rumour (the blind review: "the
                 // owner" is heard as the new owner, and Sheila does not pass on gossip).
                 "The importer's warehouse at the far end of the old warehouse row burned down last November, on a Saturday night. The evening paper called it arson, since it started in two places. Nobody was charged.", null),
            ("will", "", "Mickey left the office, Mickey's, the cab office on Quay Street, to his nephew, the new owner, by his will; the new owner came with one suitcase and a letter saying so.", null,
                 "Mickey left you the office in his will. The letter you brought says so.", null),
            ("funeral", "", "Mickey's funeral was at Father Walsh's chapel, before the new owner came; he missed it.", null,
                 "Mickey's funeral was at Father Walsh's chapel, before you came.", null),
            ("june", "june", "June, Mickey's daughter, came back to the Hook for the funeral and is still in town; she wants nothing from the office.",
                     "I came back to the Hook for my father's funeral and I am still in town; I want nothing from the office.",
                     "June, Mickey's daughter, came back for the funeral. She's still in town, and she wants nothing from the office.",
                     "I came back for my father's funeral. I'm still here, and I want nothing from the office."),
            ("flat", "", "The new owner is living in Mickey's flat over the office.", null,
                 "You're in Mickey's flat, over the office.", null),
            ("door", "lena", "The door at the back of Mickey's that Sheila does not open is Mickey's own room; it has been locked since he died, and Sheila keeps the key.",
                     "The door at the back of the office that I do not open is Mickey's own room; it has been locked since he died, and I keep the key.",
                     "The door at the back of the office that Sheila keeps shut is Mickey's own room. It's been locked since he died, and Sheila keeps the key.",
                     "The door at the back is Mickey's own room. It's been locked since he died, and I keep the key."),
            ("drivers", "", "Mickey's has two cab drivers on the rank, one by day and one by night, and a dispatcher on the radio and the phone.", null,
                 "Mickey's has two drivers on the rank, one by day and one by night, and a dispatcher on the radio and the phone.", null),
            ("hours", "", "The cab office opens at seven in the morning, nine on Sundays, and runs until the night driver goes home at three.", null,
                 "The office opens at seven, nine on a Sunday, and runs till the night driver goes home at three.", null),
            ("trade", "", "Mickey's has not made much money since the docks went; trade has been thin.", null,
                 "Mickey's hasn't made much since the docks went. Trade's been thin.", null),
            ("cafe", "", "The cafe is across the street, in the shops opposite the north end of the parade; it opens at half past six and shuts at ten at night, and on Sundays it is open only from eight till twelve.", null,
                 "The cafe's over the road, in the shops across from the north end of the parade. Half six till ten at night, and eight till twelve on a Sunday.", null),
            // WHO KEEPS WHAT AT MICKEY'S, as the whole street knows it (Jafar, 30
            // September: write down what the street would know; from the approved
            // cards, nothing new): for the rule table's plain answers (TalkRules).
            ("office", "", "Mickey's, the minicab office, is on Quay Street in the Hook, with the rank outside.", null,
                 "Mickey's is on Quay Street, with the rank outside.", null),
            // WHAT THE STREET SAYS OF MICKEY (Jafar's yes, 30 September): only these
            // two for now, the two that survived three blind reviews; for the
            // regulars who knew him (the talking cards are Sheila's, Ron's and
            // Darren's), never June, estranged, or anybody new to the street.
            ("mickey_counsel", "", "Mickey kept his business to himself; you would not hear it from him on the street.", null,
                 "Mickey kept his business to himself. You'd not hear it from him on the street.", null),
            ("mickey_kept_ron", "rocco", "Mickey kept Ron on when the docks let him go in 1989.",
                 "Mickey kept me on when the docks let me go in 1989.",
                 "Mickey kept Ron on when the docks let him go.", "Mickey kept me on when the docks let me go."),
            // Their own words start with their name, so "Who are you?" is answered
            // (the blind review); "at Mickey's", not "here", since they say it anywhere.
            ("sheila_books", "lena", "Sheila Dunn has kept the books at Mickey's for thirty-one years.",
                             "I am Sheila Dunn, and I have kept the books at Mickey's for thirty-one years.",
                             "Sheila Dunn keeps the books at Mickey's. She's been at it thirty-one years.",
                             "Sheila Dunn. I keep the books at Mickey's, and have for thirty-one years."),
            ("ron_rank", "rocco", "Ron Kirby keeps the rank outside Mickey's and watches the yard gate; Mickey kept him on when the docks let him go in 1989.",
                         "I am Ron Kirby; I keep the rank outside Mickey's and watch the yard gate, and Mickey kept me on when the docks let me go in 1989.",
                         "Ron Kirby looks after the rank outside Mickey's and watches the yard gate. Mickey kept him on when the docks let him go.",
                         "Ron Kirby. I look after the rank outside Mickey's and watch the yard gate. Mickey kept me on when the docks let me go."),
            ("darren_rounds", "sam", "Darren Milner walks Quay Street at all hours and talks to everyone; if something is being said in the Hook, he has heard it.",
                              "I am Darren Milner; I walk Quay Street at all hours and talk to everyone, and if something is being said in the Hook, I have heard it.",
                              "Darren Milner's up and down Quay Street at all hours, talking to everyone. If it's being said round here, he's heard it.",
                              "Darren. I'm up and down Quay Street at all hours, talking to everyone. If it's being said round here, I've heard it."),
        };

        /// The words a character holds a fact in, by its id (the street's, or
        /// their own when it is about them); null for an unknown id.
        public static string Held(string id, string who)
        {
            foreach (var f in All)
                if (f.id == id) return f.about.Length > 0 && f.about == who && f.own != null ? f.own : f.fact;
            return null;
        }

        /// True when `known` is a fact about `who`, in their own words.
        public static bool IsOwn(string known, string who)
        {
            if (string.IsNullOrEmpty(known) || string.IsNullOrEmpty(who)) return false;
            foreach (var f in All)
                if (f.about == who && f.own != null && f.own == known) return true;
            return false;
        }

        /// How a fact is said plainly, given the words a character holds it in
        /// (the street's, or the person's own); null for anything else, so a
        /// card's own facts, its secrets among them, are never said this way.
        public static string SaidFor(string known)
        {
            if (string.IsNullOrEmpty(known)) return null;
            foreach (var (_, _, fact, own, said, ownSaid) in All)
            {
                if (known == fact) return said;
                if (own != null && known == own) return ownSaid;
            }
            return null;
        }

        /// WHOM A FACT IS ABOUT, given the words a character holds it in (the
        /// street's or the person's own): their cast id, or null for a fact about
        /// nobody in particular, or for anything that is not a street fact. The
        /// ladder points him to them (TalkLadder): they hold it as their own.
        public static string AboutOf(string known)
        {
            if (string.IsNullOrEmpty(known)) return null;
            foreach (var f in All)
                if (known == f.fact || (f.own != null && known == f.own)) return f.about.Length > 0 ? f.about : null;
            return null;
        }

        /// WHO SOMEBODY IS, BY THEIR WORK (sheila_books, ron_rank, darren_rounds):
        /// said by anybody else, such a fact answers "who is she?" and is a pointer
        /// for everything else (TalkLadder: "You'd want Sheila for that"), never an
        /// answer to it (measured on 7 October: "What does Sheila really think of
        /// me?" answered with her thirty-one years at the books).
        public static bool IsIntroduction(string known)
        {
            if (string.IsNullOrEmpty(known)) return false;
            foreach (var f in All)
                if ((f.id == "sheila_books" || f.id == "ron_rank" || f.id == "darren_rounds") && (known == f.fact || known == f.own)) return true;
            return false;
        }

        /// The name the street says for one of the people the facts are about.
        public static string NameOf(string who) =>
            who == "lena" ? "Sheila" : who == "rocco" ? "Ron" : who == "sam" ? "Darren" : who == "june" ? "June" : null;

        /// Gives a card the street's facts for this person, once each.
        public static CharacterCard AddTo(CharacterCard card, string who)
        {
            if (card == null) return null;
            foreach (var fact in For(who))
                if (!card.HardFacts.Contains(fact)) card.HardFacts.Add(fact);
            return card;
        }

        // Facts some people on the street never hold (the Mickey lines: June is
        // estranged, Alison came a month before he died).
        static readonly Dictionary<string, string[]> NotFor = new Dictionary<string, string[]>
        {
            { "mickey_counsel", new[] { "june", "noor" } },
            { "mickey_kept_ron", new[] { "june", "noor" } },
        };

        /// What this person knows of them (a cast id; the facts about
        /// somebody else in the street's words, their own in theirs).
        public static List<string> For(string who)
        {
            var list = new List<string>();
            foreach (var (id, about, fact, own, _, _) in All)
            {
                if (NotFor.TryGetValue(id, out var not) && Array.IndexOf(not, who) >= 0) continue;
                if (about.Length > 0 && about == who) { if (own != null) list.Add(own); }
                else list.Add(fact);
            }
            return list;
        }
    }
}
