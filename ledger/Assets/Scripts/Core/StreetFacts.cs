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
        public static readonly (string about, string fact, string own, string said, string ownSaid)[] All =
        {
            ("", "Mickey died three weeks before the new owner, his nephew, came to Quay Street.", null,
                 "Mickey died three weeks before you came.", null),
            // How Mickey died (Jafar, 30 September): his heart; nobody thinks otherwise.
            ("rocco", "Mickey died of his heart, at the office early one morning; Ron found him when he came on at the rank, and the doctor said it was his heart.",
                      "I found Mickey at the office early one morning, when I came on at the rank; the doctor said it was his heart.",
                      "It was his heart. Ron found him at the office early one morning, coming on at the rank.",
                      "It was his heart. I found him at the office early one morning, when I came on at the rank."),
            // The warehouse fire as the street has it (Jafar, 30 September); the truth is never the street's.
            ("", "Last November, on a Saturday night, the importer's warehouse at the far end of the old warehouse row burned down; the evening paper called it arson, since it started in two places, but nobody was charged, and the street says the owner had it done for the insurance.", null,
                 "The importer's warehouse on the old row burned down last November, on a Saturday night. The paper called it arson. Nobody was charged, and the street says the owner had it done for the insurance.", null),
            ("", "Mickey left the office, Mickey's, the cab office on Quay Street, to his nephew, the new owner, by his will; the new owner came with one suitcase and a letter saying so.", null,
                 "Mickey left you the office in his will. You came with one suitcase and the letter saying so.", null),
            ("", "Mickey's funeral was at Father Walsh's chapel, before the new owner came; he missed it.", null,
                 "The funeral was at Father Walsh's chapel, before you came.", null),
            ("june", "June, Mickey's daughter, came back to the Hook for the funeral and is still in town; she wants nothing from the office.",
                     "I came back to the Hook for my father's funeral and I am still in town; I want nothing from the office.",
                     "June, Mickey's daughter, came back for the funeral. She's still in town, and she wants nothing from the office.",
                     "I came back for my father's funeral. I'm still here, and I want nothing from the office."),
            ("", "The new owner is living in Mickey's flat over the office.", null,
                 "You're in Mickey's flat, over the office.", null),
            ("lena", "The door at the back of Mickey's that Sheila does not open is Mickey's own room; it has been locked since he died, and Sheila keeps the key.",
                     "The door at the back of the office that I do not open is Mickey's own room; it has been locked since he died, and I keep the key.",
                     "That back door at Mickey's is Mickey's own room. It's been locked since he died, and Sheila keeps the key.",
                     "That's Mickey's own room. It's been locked since he died, and I keep the key."),
            ("", "Mickey's has two cab drivers on the rank, one by day and one by night, and a dispatcher on the radio and the phone.", null,
                 "Two drivers on the rank, one by day and one by night, and a dispatcher on the radio and the phone.", null),
            ("", "The cab office opens at seven in the morning, nine on Sundays, and runs until the night driver goes home at three.", null,
                 "The office opens at seven, nine on a Sunday, and runs till the night driver goes home at three.", null),
            ("", "Mickey's has not made much money since the docks went; trade has been thin.", null,
                 "Mickey's hasn't made much since the docks went. Trade's been thin.", null),
            ("", "The cafe is across the street, in the shops opposite the north end of the parade; it opens at half past six and shuts at ten at night, and on Sundays it is open only from eight till twelve.", null,
                 "The cafe's across the street, opposite the north end of the parade. Half six till ten at night, and eight till twelve on a Sunday.", null),
        };

        /// How a fact is said plainly, given the words a character holds it in
        /// (the street's, or the person's own); null for anything else, so a
        /// card's own facts, its secrets among them, are never said this way.
        public static string SaidFor(string known)
        {
            if (string.IsNullOrEmpty(known)) return null;
            foreach (var (_, fact, own, said, ownSaid) in All)
            {
                if (known == fact) return said;
                if (own != null && known == own) return ownSaid;
            }
            return null;
        }

        /// Gives a card the street's facts for this person, once each.
        public static CharacterCard AddTo(CharacterCard card, string who)
        {
            if (card == null) return null;
            foreach (var fact in For(who))
                if (!card.HardFacts.Contains(fact)) card.HardFacts.Add(fact);
            return card;
        }

        /// What this person knows of them (a cast id; the facts about
        /// somebody else in the street's words, their own in theirs).
        public static List<string> For(string who)
        {
            var list = new List<string>();
            foreach (var (about, fact, own, _, _) in All)
            {
                if (about.Length > 0 && about == who) { if (own != null) list.Add(own); }
                else list.Add(fact);
            }
            return list;
        }
    }
}
